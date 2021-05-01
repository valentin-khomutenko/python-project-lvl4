import pytest
import django.test
from http import HTTPStatus

from task_manager.statuses.models import Status


@pytest.mark.django_db
def test_get_status_fails_if_not_logged_in(client: django.test.Client):
    response = client.get('/statuses/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/?next=/statuses/'


@pytest.mark.django_db
def test_get_statuses(logged_in_client: django.test.Client):
    response = logged_in_client.get('/statuses/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_create_status_fails_if_not_logged_in(client: django.test.Client):
    response = client.get('/statuses/create/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/?next=/statuses/create/'


@pytest.mark.django_db
def test_create_status(logged_in_client: django.test.Client):
    response = logged_in_client.get('/statuses/create/')
    assert response.status_code == HTTPStatus.OK

    response = logged_in_client.post('/statuses/create/', data={'name': 'Done'})
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/statuses/'


@pytest.mark.django_db
def test_create_status_fails_if_name_is_not_unique(logged_in_client: django.test.Client):
    Status(name='Done').save()
    response = logged_in_client.post('/statuses/create/', data={'name': 'Done'})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.django_db
def test_delete_status_fails_if_not_logged_in(client: django.test.Client):
    status = Status(name='Done')
    status.save()

    response = client.get(f'/statuses/{status.pk}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/statuses/{status.pk}/delete/'

    response = client.post(f'/statuses/{status.pk}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/statuses/{status.pk}/delete/'

    status.refresh_from_db()
    assert status.pk is not None


@pytest.mark.django_db
def test_delete_status(logged_in_client: django.test.Client):
    status = Status(name='Done')
    status.save()

    response = logged_in_client.get(f'/statuses/{status.pk}/delete/')
    assert response.status_code == HTTPStatus.OK

    response = logged_in_client.post(f'/statuses/{status.pk}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/statuses/'

    response = logged_in_client.get(f'/statuses/{status.pk}/delete/')
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_update_status_fails_if_not_logged_in(client: django.test.Client):
    status = Status(name='Done')
    status.save()

    response = client.get(f'/statuses/{status.pk}/update/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/statuses/{status.pk}/update/'

    response = client.post(f'/statuses/{status.pk}/update/', data={'name': 'Finished'})
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/statuses/{status.pk}/update/'

    status.refresh_from_db()
    assert status.name == 'Done'


@pytest.mark.django_db
def test_update_status(logged_in_client: django.test.Client):
    status = Status(name='Done')
    status.save()

    response = logged_in_client.get(f'/statuses/{status.pk}/update/')
    assert response.status_code == HTTPStatus.OK

    response = logged_in_client.post(f'/statuses/{status.pk}/update/', data={'name': 'Finished'})
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/statuses/'

    status.refresh_from_db()
    assert status.name == 'Finished'


@pytest.mark.django_db
def test_update_status_fails_if_name_is_not_unique(logged_in_client: django.test.Client):
    Status(name='Done').save()
    status = Status(name='Finished')
    status.save()

    response = logged_in_client.post(f'/statuses/{status.pk}/update/', data={'name': 'Done'})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
