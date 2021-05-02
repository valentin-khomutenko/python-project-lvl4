from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView  # type: ignore

from task_manager.mixins.views import RaiseUnprocessableEnittyIfInvalidMixin
from task_manager.tasks import models
from task_manager.tasks import filters


class ListTasks(LoginRequiredMixin, FilterView):
    filterset_class = filters.TaskFilter
    template_name = 'tasks/list.html'


class CreateTask(LoginRequiredMixin, RaiseUnprocessableEnittyIfInvalidMixin, CreateView):
    model = models.Task
    template_name = 'tasks/create.html'
    fields = ('name', 'description', 'executor', 'status', 'labels',)
    success_url = reverse_lazy('list_tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = models.Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('list_tasks')


class UpdateTask(LoginRequiredMixin, UpdateView):
    model = models.Task
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('list_tasks')

    fields = ('name', 'description', 'executor', 'status', 'labels',)
