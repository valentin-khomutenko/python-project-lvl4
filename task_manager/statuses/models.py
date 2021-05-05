from django.db import models
from django.utils.translation import gettext as _

MAX_STATUS_NAME_LENGTH = 100


# TODO: localisation for fields
class Status(models.Model):
    name = models.CharField(max_length=MAX_STATUS_NAME_LENGTH, unique=True, verbose_name=_('Name'))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_('Created at'))

    def __str__(self):
        return self.name
