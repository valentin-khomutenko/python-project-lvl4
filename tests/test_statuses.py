import pytest
import django.test
from http import HTTPStatus


@pytest.mark.django_db
def test_get_statuses(client: django.test.Client, django_user_model):
    response = client.get('/statuses/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/?next=/statuses/'

    user = django_user_model.objects.create_user(username='testuser', password='mysecretpass')
    user.save()

    logged_in = client.login(username=user.username, password='mysecretpass')
    assert logged_in

    response = client.get('/statuses/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_create_status(client: django.test.Client, django_user_model):
    response = client.get('/statuses/create/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/?next=/statuses/create/'

    user = django_user_model.objects.create_user(username='testuser', password='mysecretpass')
    user.save()

    logged_in = client.login(username=user.username, password='mysecretpass')
    assert logged_in

    response = client.get('/statuses/create/')
    assert response.status_code == HTTPStatus.OK

    response = client.post('/statuses/create/', data={'name': 'Done'})
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/statuses/'

    response = client.post('/statuses/create/', data={'name': 'Done'})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
