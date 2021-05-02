from django.db import models


MAX_STATUS_NAME_LENGTH = 100


# TODO: localisation for fields
class Status(models.Model):
    name = models.CharField(max_length=MAX_STATUS_NAME_LENGTH, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name
