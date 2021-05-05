import django.contrib.auth
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from . import forms
from . import mixins
from task_manager.mixins.views import RaiseUnprocessableEnittyIfInvalidMixin, \
    SuccessMessageDeleteMixin


class CreateUser(SuccessMessageMixin, RaiseUnprocessableEnittyIfInvalidMixin, CreateView):
    model = django.contrib.auth.get_user_model()
    form_class = forms.CreateUser
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('User has been created')


class ListUsers(ListView):
    model = django.contrib.auth.get_user_model()
    template_name = 'users/list.html'


class DeleteUser(SuccessMessageDeleteMixin, mixins.CheckSelfUser, DeleteView):
    model = django.contrib.auth.get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('list_users')
    success_message = _('User has been deleted')

    def delete(self, request, *args, **kwargs):
        if self.get_object().author.all().exists() or self.get_object().executor.all().exists():
            messages.error(
                self.request,
                _('User cannot be deleted as they are referenced as either author or executor')
            )
            return redirect('list_users')

        return super().delete(request, *args, **kwargs)


class UpdateUser(SuccessMessageMixin, RaiseUnprocessableEnittyIfInvalidMixin,
                 mixins.CheckSelfUser, UpdateView):
    model = django.contrib.auth.get_user_model()
    template_name = 'users/update.html'
    form_class = forms.CreateUser
    success_url = reverse_lazy('list_users')
    success_message = _('User has been updated')
