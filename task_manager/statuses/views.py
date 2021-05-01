from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms
from task_manager.mixins.views import RaiseUnprocessableEnittyIfInvalidMixin  # type: ignore


class ListStatuses(LoginRequiredMixin, ListView):
    model = models.Status
    template_name = 'statuses/list.html'


class CreateStatus(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin, CreateView):
    model = models.Status
    success_url = reverse_lazy('list_statuses')
    form_class = forms.StatusForm
    template_name = 'statuses/create.html'


class DeleteStatus(LoginRequiredMixin, DeleteView):
    model = models.Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('list_statuses')


class UpdateStatus(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin, UpdateView):
    model = models.Status
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('list_statuses')
    fields = ('name',)
