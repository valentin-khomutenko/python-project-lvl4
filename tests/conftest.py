import django.test
import pytest


@pytest.fixture
def make_test_user(django_user_model):
    def _make_user(username='johndoe',
                   first_name='John',
                   last_name='Doe',
                   password='topsecret123'):
        user = django_user_model.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        return user, password
    return _make_user


@pytest.fixture
def logged_in_client(client: django.test.Client, make_test_user):
    user, password = make_test_user()
    client.login(username=user.username, password=password)
    return client
