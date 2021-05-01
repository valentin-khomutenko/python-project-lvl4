from http import HTTPStatus
import django.test
import pytest


@pytest.mark.django_db
def test_login_fails_with_non_existing_credentials(client: django.test.Client):
    response = client.post('/login/', data={
        'username': 'johndoe',
        'password': 'topsecret123',
    })
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
def test_login_successful_with_existing_credentials(client: django.test.Client, make_test_user):
    user, password = make_test_user()
    response = client.post('/login/', data={
        'username': user.username,
        'password': password
    })
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/'


@pytest.mark.django_db
def test_sign_up(client: django.test.Client):
    response = client.get('/users/create/')
    assert response.status_code == HTTPStatus.OK

    response = client.post('/users/create/', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'password1': 'topsecret123',
        'password2': 'topsecret123',
    })
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/'


@pytest.mark.django_db
def test_sign_up_fails_is_username_exists(client: django.test.Client, make_test_user):
    user, _ = make_test_user()

    response = client.post('/users/create/', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'username': user.username,
        'password1': 'topsecret123',
        'password2': 'topsecret123',
    })
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
