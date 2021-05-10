from django import forms
from django.utils import timezone
from django.forms import widgets
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from projects.models import Project, TaskForProject, TaskForDeal


class ProjectCreateForm(forms.ModelForm):
    field_order = [
        'name',
        'payment',
        'begin_date',
        'end_date',
        'description'
    ]
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Название'})
        self.fields['begin_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'

    class Meta:
        model = Project
        exclude = [
            'created_by',
            'creation_datetime',
            'update_datetime',
        ]
        labels = {
            'name': 'Название',
            'payment': 'Сумма',
            'description': 'Описание',
            'begin_date': 'Дата начала',
            'end_date': 'Дата окончания',
        }


class ProjectUpdateForm(forms.Form):
    name = forms.CharField(max_length=100)

    begin_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'template-class'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'template-class'}))
    payment = forms.IntegerField(
        label="Сумма контракта",
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'id': 'description' ,'class': 'special'}),
    )

# Task forms and formset

class TaskCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assign'].required = False
        self.fields['begin_date'].widget.input_type = "date"
        self.fields['begin_date'].help_text = "ГГ-ММ-ДД"
        self.fields['end_date'].widget.input_type = "date"
        self.fields['end_date'].help_text = "ГГ-ММ-ДД"

    class Meta:
        model = TaskForProject
        labels = {
            'task_name': 'Название задачи',
            'assign': 'Исполнитель задачи',
            'begin_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'status': 'Статус задачи',
            'priority': 'Приоритет',
            'description': 'Описание',
        }

        exclude = ('creation_datetime', 'update_datetime',)


class HiddenDeleteBaseInlineFormSet(BaseInlineFormSet):
    """
    Makes the delete field a hidden input rather than the default checkbox
    inlineformset_factory(Book, Page, formset=HiddenDeleteBaseInlineFormSet, can_delete=True)
    """
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['DELETE'] = forms.BooleanField(
            label='Delete',
            required=False,
            widget=forms.widgets.HiddenInput
        )

TaskForProjectFormSet = inlineformset_factory(
    Project,
    TaskForProject,
    form=TaskCreateForm,
    formset=HiddenDeleteBaseInlineFormSet,
    fields='__all__',
    extra=1,
    max_num=5,
    can_delete=True,
)

class TaskUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task_name'].widget.attrs.update({'class': 'w-100'})
        self.fields['begin_date'].widget.attrs.update({'class': 'w-100'})
        self.fields['end_date'].widget.attrs.update({'class': 'w-100'})
        self.fields['assign'].widget.attrs.update({'class': 'w-100'})
        self.fields['status'].widget.attrs.update({'class': 'w-100'})

    class Meta:
        model = TaskForProject
        fields = ['task_name', 'assign', 'begin_date', 'end_date', 'status', 'description']
        labels = {
            'task_name': 'Название',
            'assign': "Назначен",
            'status': "Статус",
        }
