from http import HTTPStatus

import django.test
import pytest


@pytest.mark.django_db
def test_create_user(client: django.test.Client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_delete_user(client: django.test.Client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='mysecretpass')
    user.save()

    logged_in = client.login(username=user.username, password='mysecretpass')
    assert logged_in

    response = client.get(f'/users/{user.id}/delete/')
    assert response.status_code == HTTPStatus.OK

    response = client.post(f'/users/{user.id}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/'

    response = client.get(f'/users/{user.id}/delete/')
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_user_can_delete_only_themselves(client: django.test.Client, django_user_model):
    self = django_user_model.objects.create_user(username='testuser', password='mysecretpass')
    self.save()

    other_user = django_user_model.objects.create_user(username='testuser2', password='mysecretpass')
    other_user.save()

    logged_in = client.login(username=self.username, password='mysecretpass')
    assert logged_in

    response = client.get(f'/users/{self.id}/delete/')
    assert response.status_code == HTTPStatus.OK

    response = client.get(f'/users/{other_user.id}/delete/')
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = client.post(f'/users/{other_user.id}/delete/')
    assert response.status_code == HTTPStatus.FORBIDDEN

