from django.contrib.auth import get_user_model
from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(to=Status, on_delete=models.PROTECT)
    executor = models.ForeignKey(to=get_user_model(), blank=True, null=True, on_delete=models.PROTECT,
                                 related_name='executor')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT, related_name='author')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    labels = models.ManyToManyField(to=Label, null=True, blank=True)
