import django.contrib.auth
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from . import forms
from . import mixins


class CreateUser(SuccessMessageMixin, CreateView):
    model = django.contrib.auth.get_user_model()
    form_class = forms.CreateUser
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')


class ListUsers(ListView):
    model = django.contrib.auth.get_user_model()
    template_name = 'users/list.html'


class DeleteUser(SuccessMessageMixin, mixins.CheckSelfUser, DeleteView):
    model = django.contrib.auth.get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('login')


class UpdateUser(SuccessMessageMixin, mixins.CheckSelfUser, UpdateView):
    model = django.contrib.auth.get_user_model()
    template_name = 'users/update.html'
    form_class = forms.CreateUser
    success_url = reverse_lazy('list_users')
