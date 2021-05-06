from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from . import models
from task_manager.mixins.views import RaiseUnprocessableEnittyIfInvalidMixin, \
    SuccessMessageDeleteMixin


class ListStatuses(LoginRequiredMixin, ListView):
    model = models.Status
    template_name = 'statuses/list.html'


class CreateStatus(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin,
                   SuccessMessageMixin, CreateView):
    model = models.Status
    success_url = reverse_lazy('list_statuses')
    success_message = _('Status has been created')
    template_name = 'statuses/create.html'
    fields = ('name',)


class DeleteStatus(LoginRequiredMixin, SuccessMessageDeleteMixin, DeleteView):
    model = models.Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('list_statuses')
    success_message = _('Status has been deleted')

    def delete(self, request, *args, **kwargs):
        if self.get_object().task_set.all().exists():
            messages.error(self.request, _('Unable to delete status because it is in use'))
            return redirect('list_statuses')
        return super().delete(request, *args, **kwargs)


class UpdateStatus(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin,
                   SuccessMessageMixin, UpdateView):
    model = models.Status
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('list_statuses')
    success_message = _('Status has been updated')
    fields = ('name',)
