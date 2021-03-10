from http import HTTPStatus

import django.test
import pytest


@pytest.mark.django_db
def test_auth(client: django.test.Client):
    user_password = 'topsecret'
    user_name = 'johndoe'
    login_form = {
        'username': user_name,
        'password': user_password,
    }
    create_user_form = {
        'username': user_name,
        'password': user_password,
    }

    response = client.post('/login/', data=login_form)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = client.post('/users/create/', data=create_user_form)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/'

    response = client.post('/login/', data=login_form)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/'
