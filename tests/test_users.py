from http import HTTPStatus

import django.test
import pytest


@pytest.mark.django_db
def test_create_user(client: django.test.Client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
