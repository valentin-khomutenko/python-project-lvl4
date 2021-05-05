from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django_filters.views import FilterView  # type: ignore
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _

from task_manager.mixins.views import RaiseUnprocessableEnittyIfInvalidMixin, \
    SuccessMessageDeleteMixin
from task_manager.tasks import models
from task_manager.tasks import filters


class ListTasks(LoginRequiredMixin, FilterView):
    filterset_class = filters.TaskFilter
    template_name = 'tasks/list.html'


class CreateTask(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin,
                 SuccessMessageMixin, CreateView):
    model = models.Task
    template_name = 'tasks/create.html'
    fields = ('name', 'description', 'executor', 'status', 'labels',)
    success_url = reverse_lazy('list_tasks')
    success_message = _('Task has been created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeleteTask(LoginRequiredMixin, SuccessMessageDeleteMixin, DeleteView):
    model = models.Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('list_tasks')
    success_message = _('Task has been deleted')


class UpdateTask(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.Task
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('list_tasks')
    success_message = _('Task has been updated')

    fields = ('name', 'description', 'executor', 'status', 'labels',)


class TaskDetail(LoginRequiredMixin, DetailView):
    model = models.Task
    template_name = 'tasks/detail.html'
