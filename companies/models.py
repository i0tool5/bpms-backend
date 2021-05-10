import uuid


from django.db import models

from companies.validators import phone_num_validator


class AbstractClient(models.Model):
    uid = models.UUIDField(editable=False, primary_key=True, unique=True, default=uuid.uuid4)
    name = models.fields.CharField(
        max_length=127,
        null=False,
        blank=False,
        unique=True
    )
    phone_num_1 = models.fields.CharField(
        max_length=12,
        null=False,
        blank=False,
        validators=[phone_num_validator]
    )
    phone_num_2 = models.fields.CharField(
        max_length=12,
        null=True,
        blank=True,
        validators=[phone_num_validator]
    )
    e_mail = models.fields.EmailField(
        null=True,
        blank=True
    )
    class Meta:
        ordering = ['name']
        abstract = True

    def __str__(self):
        return self.name


class Company(AbstractClient):
    addr = models.fields.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    class Meta(AbstractClient.Meta):
        abstract = False
        indexes = [
            models.Index(fields=['name'])
        ]


class Contact(AbstractClient):
    company = models.fields.CharField(
        max_length=127,
        null=True,
        blank=True
    )
