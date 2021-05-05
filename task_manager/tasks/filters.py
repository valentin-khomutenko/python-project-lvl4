from django import forms

from task_manager.labels.models import Label
from task_manager.tasks import models
from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter  # type: ignore
from django.utils.translation import gettext as _


class TaskFilter(FilterSet):
    self_tasks = BooleanFilter(
        label=_('Self tasks'), method='filter_self_tasks', widget=forms.CheckboxInput
    )
    label = ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label=_('Label'),
    )

    class Meta:
        model = models.Task
        fields = ('status', 'executor', 'label', 'self_tasks')

    def filter_self_tasks(self, queryset, name, value):
        if value:
            queryset = queryset.filter(author=self.request.user)
        return queryset
