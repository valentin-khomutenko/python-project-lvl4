from django import forms

from task_manager.tasks import models
from django_filters import FilterSet, BooleanFilter  # type: ignore


class TaskFilter(FilterSet):
    self_tasks = BooleanFilter(
        label='self_tasks', method='filter_self_tasks', widget=forms.CheckboxInput)

    class Meta:
        model = models.Task
        fields = ('status', 'executor', 'labels')

    def filter_self_tasks(self, queryset, name, value):
        if value:
            queryset = queryset.filter(author=self.request.user)
        return queryset
