from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _

from task_manager.labels import models
from task_manager.mixins.views import RaiseUnprocessableEnittyIfInvalidMixin, \
    SuccessMessageDeleteMixin


class ListLabels(LoginRequiredMixin, ListView):
    model = models.Label
    template_name = 'labels/list.html'


class CreateLabel(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin, SuccessMessageMixin, CreateView):
    model = models.Label
    template_name = 'labels/create.html'

    fields = ('name',)
    success_url = reverse_lazy('list_labels')
    success_message = _('Label has been created')


class DeleteLabel(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin, SuccessMessageDeleteMixin, DeleteView):
    model = models.Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('list_labels')
    success_message = _('Label has been deleted')


class UpdateLabel(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin, SuccessMessageMixin, UpdateView):
    model = models.Label
    template_name = 'labels/update.html'
    success_url = reverse_lazy('list_labels')
    success_message = _('Label has been updated')
    fields = ('name',)
