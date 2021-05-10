import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class MainAbstractModel(models.Model):
    uid = models.UUIDField(editable=False, primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=128)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering = ['-creation_datetime']


class DealProjAbstractModel(MainAbstractModel):
    payment = models.IntegerField(default=100_000, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    public = models.BooleanField(default=False, blank=False)
    
    @classmethod
    def get_payment_sum(cls):
        return cls.objects.aggregate(models.Sum('payment'))
    
    def __str__(self):
        return self.name
    
    class Meta(MainAbstractModel.Meta):
        abstract = True


class Status(models.Model):
    '''This class represents statuses for deals'''
    uid = models.UUIDField(editable=False, primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Deal(DealProjAbstractModel):
    client = models.CharField(max_length=128, default='', null=True, blank=True) 
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='deals_created',
        null=True,
        )
    assigned = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='deals',
        )


class Project(DealProjAbstractModel):
    begin_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='projects',
        null=True,
        )
    
    class Meta:
        ordering = ["-creation_datetime"]


class TaskModel(models.Model):
    uid = models.UUIDField(editable=False, primary_key=True, unique=True, default=uuid.uuid4)
    statuses = (('1', 'Открыта'), ('2', 'В работе'), ('3', 'Закрыта'))
    prio = (('1', 'Низкий'), ('2', 'Ниже среднего'), ('3', 'Средний'), ('4', 'Выше среднего'), ('5', 'Высокий'), ('6', 'Реального времени'))

    name = models.CharField(max_length=80)
    assign = models.ManyToManyField(
        get_user_model(),
        related_name='tasks',
        )
    begin_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=7, choices=statuses, default=1)
    priority = models.CharField(max_length=10, choices=prio, default=3)
    description = models.TextField(max_length=512, null=True, blank=True)

    created_by = models.ForeignKey(get_user_model(), related_name='tasks_created', on_delete=models.SET_NULL, null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    # generic relation to projects/deals
    content_type = models.ForeignKey(ContentType,
                                        on_delete=models.CASCADE,
                                    )
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['end_date', 'name']
