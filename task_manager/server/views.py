from http import HTTPStatus

import django.contrib.auth.views
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'index.html'


class Login(django.contrib.auth.views.LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form),
                                       status=HTTPStatus.UNAUTHORIZED)


class Logout(django.contrib.auth.views.LogoutView):
    pass
