from django.db import models
from django.utils.translation import gettext as _


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_('Created at'))

    def __str__(self):
        return self.name
