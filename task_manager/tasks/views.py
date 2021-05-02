from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from task_manager.mixins.views import RaiseUnprocessableEnittyIfInvalidMixin
from task_manager.tasks import models


class ListTasks(LoginRequiredMixin, ListView):
    template_name = 'tasks/list.html'

    def get_queryset(self):
        queryset = models.Task.objects
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        executor_filter = self.request.GET.get('executor')
        if executor_filter:
            queryset = queryset.filter(executor=executor_filter)

        label_filter = self.request.GET.get('label')
        if label_filter:
            queryset = queryset.filter(labels__id=label_filter)

        self_task_filter = self.request.GET.get('self_task')
        if self_task_filter:
            queryset = queryset.filter(author=self.request.user)
        return queryset


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
