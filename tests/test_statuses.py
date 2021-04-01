import pytest
import django.test
from http import HTTPStatus


@pytest.mark.django_db
def test_get_statuses(client: django.test.Client):
    response = client.get('/statuses/')
    assert response.status_code == HTTPStatus.OK
