from http import HTTPStatus

import django.contrib.auth.views
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext as _


class Index(TemplateView):
    template_name = 'index.html'


class Login(SuccessMessageMixin, django.contrib.auth.views.LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    success_message = _('You are logged in')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form),
                                       status=HTTPStatus.UNAUTHORIZED)


class Logout(django.contrib.auth.views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
