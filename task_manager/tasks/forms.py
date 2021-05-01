from django.forms.models import ModelForm

from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude: list[str] = []
