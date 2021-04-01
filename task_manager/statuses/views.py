from django.views.generic import ListView
from . import models


class ListStatuses(ListView):
    model = models.Status
    template_name = 'statuses/list.html'
