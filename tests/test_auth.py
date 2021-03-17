from http import HTTPStatus

import django.test
import pytest


def test_index(client: django.test.Client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_sign_up_and_login(client: django.test.Client):
    user = make_user(first_name='John', last_name='Doe', user_name='johndoe',
                     password='topsecret123')
    login_form = make_login_form(user)
    create_user_form = make_create_user_form(user)

    response = client.post('/login/', data=login_form)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = client.get('/users/create/')
    assert response.status_code == HTTPStatus.OK

    response = client.post('/users/create/', data=create_user_form)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/'

    response = client.post('/login/', data=login_form)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/'


def make_user(first_name, last_name, user_name, password):
    return first_name, last_name, user_name, password


def make_login_form(user):
    _, _, user_name, user_password = user
    return {
        'username': user_name,
        'password': user_password
    }


def make_create_user_form(user):
    user_first_name, user_last_name, user_name, user_password = user

    return {
        'first_name': user_first_name,
        'last_name': user_last_name,
        'username': user_name,
        'password1': user_password,
        'password2': user_password,
    }
