import django.contrib.auth
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms


class CreateUser(SuccessMessageMixin, CreateView):
    model = django.contrib.auth.get_user_model()
    form_class = forms.CreateUser
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
