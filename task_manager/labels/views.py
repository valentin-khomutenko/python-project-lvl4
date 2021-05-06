from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
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


class CreateLabel(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin,
                  SuccessMessageMixin, CreateView):
    model = models.Label
    template_name = 'labels/create.html'

    fields = ('name',)
    success_url = reverse_lazy('list_labels')
    success_message = _('Label has been created')


class DeleteLabel(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin,
                  SuccessMessageDeleteMixin, DeleteView):
    model = models.Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('list_labels')
    success_message = _('Label has been deleted')

    def delete(self, request, *args, **kwargs):
        if self.get_object().task_set.all().exists():
            messages.error(self.request, _('Unable to delete label because it is in use'))
            return redirect('list_labels')
        return super().delete(request, *args, **kwargs)


class UpdateLabel(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin,
                  SuccessMessageMixin, UpdateView):
    model = models.Label
    template_name = 'labels/update.html'
    success_url = reverse_lazy('list_labels')
    success_message = _('Label has been updated')
    fields = ('name',)
