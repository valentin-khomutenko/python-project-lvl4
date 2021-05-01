from http import HTTPStatus

import django.test


def test_index(client: django.test.Client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
