import django.forms


class CreateUser(django.forms.Form):
    username = django.forms.CharField()
    password = django.forms.CharField(widget=django.forms.PasswordInput)


class Login(django.forms.Form):
    username = django.forms.CharField()
    password = django.forms.CharField(widget=django.forms.PasswordInput)
