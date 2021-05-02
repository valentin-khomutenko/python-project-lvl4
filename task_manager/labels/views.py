from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from task_manager.labels import models
from task_manager.mixins.views import RaiseUnprocessableEnittyIfInvalidMixin


class ListLabels(LoginRequiredMixin, ListView):
    model = models.Label
    template_name = 'labels/list.html'


class CreateLabel(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin, CreateView):
    model = models.Label
    template_name = 'labels/create.html'

    fields = ('name',)
    success_url = reverse_lazy('list_labels')


class DeleteLabel(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin, DeleteView):
    model = models.Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('list_labels')


class UpdateLabel(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin, UpdateView):
    model = models.Label
    template_name = 'labels/update.html'
    success_url = reverse_lazy('list_labels')
    fields = ('name',)
