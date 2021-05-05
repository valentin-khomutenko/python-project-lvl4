from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    status = models.ForeignKey(to=Status, on_delete=models.PROTECT, verbose_name=_('Status'))
    executor = models.ForeignKey(to=get_user_model(), blank=True, null=True, on_delete=models.PROTECT,
                                 related_name='executor', verbose_name=_('Executor'))
    author = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT, related_name='author', verbose_name=_('Author'))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_('Created at'))

    labels = models.ManyToManyField(to=Label, null=True, blank=True, verbose_name=_('Labels'))
