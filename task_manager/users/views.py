from http import HTTPStatus

import django.views
import django.shortcuts
import django.urls
import django.contrib.auth
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from . import forms


class CreateUser(django.views.View):
    def post(self, request: HttpRequest, *args, **kwargs):
        form = forms.CreateUser(request.POST)
        if not form.is_valid():
            return HttpResponse(status=HTTPStatus.UNPROCESSABLE_ENTITY)
        data = form.cleaned_data

        user = User.objects.create_user(username=data['username'], password=data['password'])
        user.save()
        return django.shortcuts.redirect(django.urls.reverse('login'))


class Login(django.views.View):
    def post(self, request: HttpRequest, *args, **kwargs):
        form = forms.Login(request.POST)
        if not form.is_valid():
            return HttpResponse(status=HTTPStatus.UNPROCESSABLE_ENTITY)
        data = form.cleaned_data
        user = django.contrib.auth.authenticate(username=data['username'],
                                                password=data['password'])
        if user is None:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

        django.contrib.auth.login(request, user)
        return django.shortcuts.redirect(django.urls.reverse('index'))
