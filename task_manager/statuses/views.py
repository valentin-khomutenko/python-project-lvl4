from http import HTTPStatus

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms


class ListStatuses(LoginRequiredMixin, ListView):
    model = models.Status
    template_name = 'statuses/list.html'


class CreateStatus(LoginRequiredMixin, CreateView):
    model = models.Status
    success_url = reverse_lazy('list_statuses')
    form_class = forms.StatusForm
    template_name = 'statuses/create.html'

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form),
                                       status=HTTPStatus.UNPROCESSABLE_ENTITY)
