import pytest
import django.test
from http import HTTPStatus

from task_manager.statuses.models import Status


@pytest.mark.django_db
def test_get_statuses_requires_login(client: django.test.Client):
    response = client.get('/statuses/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/?next=/statuses/'


@pytest.mark.django_db
def test_get_statuses(client: django.test.Client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='mysecretpass')
    user.save()

    logged_in = client.login(username=user.username, password='mysecretpass')
    assert logged_in

    response = client.get('/statuses/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_create_status_requires_login(client: django.test.Client):
    response = client.get('/statuses/create/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/?next=/statuses/create/'


@pytest.mark.django_db
def test_create_status(client: django.test.Client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='mysecretpass')
    user.save()

    logged_in = client.login(username=user.username, password='mysecretpass')
    assert logged_in

    response = client.get('/statuses/create/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_status_name_is_unique(client: django.test.Client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='mysecretpass')
    user.save()

    logged_in = client.login(username=user.username, password='mysecretpass')
    assert logged_in

    Status(name='Done').save()

    response = client.post('/statuses/create/', data={'name': 'Done'})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.django_db
def test_delete_status_requires_login(client: django.test.Client):
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
def test_delete_status(client: django.test.Client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='mysecretpass')
    user.save()

    logged_in = client.login(username=user.username, password='mysecretpass')
    assert logged_in

    status = Status(name='Done')
    status.save()

    response = client.get(f'/statuses/{status.pk}/delete/')
    assert response.status_code == HTTPStatus.OK

    response = client.post(f'/statuses/{status.pk}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/statuses/'

    response = client.get(f'/statuses/{status.pk}/delete/')
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_update_status_requires_login(client: django.test.Client):
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
def test_update_status(client: django.test.Client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='mysecretpass')
    user.save()

    logged_in = client.login(username=user.username, password='mysecretpass')
    assert logged_in

    status = Status(name='Done')
    status.save()

    response = client.get(f'/statuses/{status.pk}/update/')
    assert response.status_code == HTTPStatus.OK

    response = client.post(f'/statuses/{status.pk}/update/', data={'name': 'Finished'})
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/statuses/'

    status.refresh_from_db()
    assert status.name == 'Finished'


@pytest.mark.django_db
def test_status_name_is_unique_checked_when_update(client: django.test.Client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='mysecretpass')
    user.save()

    logged_in = client.login(username=user.username, password='mysecretpass')
    assert logged_in

    Status(name='Done').save()
    status = Status(name='Finished')
    status.save()

    response = client.post(f'/statuses/{status.pk}/update/', data={'name': 'Done'})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
