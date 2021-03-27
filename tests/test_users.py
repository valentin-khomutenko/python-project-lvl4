from http import HTTPStatus

import django.test
import pytest


@pytest.mark.django_db
def test_get_users(client: django.test.Client):
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
def test_only_logged_in_client_can_perform_delete(client: django.test.Client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='mysecretpass')
    user.save()
    user_id = user.id

    response = client.get(f'/users/{user_id}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/users/{user_id}/delete/'

    response = client.post(f'/users/{user_id}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/users/{user_id}/delete/'

    user.refresh_from_db()
    assert user.id == user_id


@pytest.mark.django_db
def test_user_can_delete_only_themselves(client: django.test.Client, django_user_model):
    self = django_user_model.objects.create_user(username='testuser', password='mysecretpass')
    self.save()

    other_user = django_user_model.objects.create_user(
        username='testuser2', password='mysecretpass')
    other_user.save()
    other_user_id = other_user.id

    logged_in = client.login(username=self.username, password='mysecretpass')
    assert logged_in

    response = client.get(f'/users/{other_user_id}/delete/')
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = client.post(f'/users/{other_user_id}/delete/')
    assert response.status_code == HTTPStatus.FORBIDDEN

    other_user.refresh_from_db()
    assert other_user.id == other_user_id


@pytest.mark.django_db
def test_update_user(client: django.test.Client, django_user_model):
    user = django_user_model.objects.create_user(
        username='testuser',
        first_name='John',
        last_name='Doe',
        password='mysecretpass'
    )
    user.save()

    logged_in = client.login(username=user.username, password='mysecretpass')
    assert logged_in

    response = client.get(f'/users/{user.id}/update/')
    assert response.status_code == HTTPStatus.OK

    update_form = {
       'username': 'testuser_updated',
        'first_name': 'John_updated',
        'last_name': 'Doe_updated',
        'password1': 'mysecretpass',
        'password2': 'mysecretpass',
    }
    response = client.post(f'/users/{user.id}/update/', update_form)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/users/'

    user.refresh_from_db()
    assert user.username == 'testuser_updated'
    assert user.first_name == 'John_updated'
    assert user.last_name == 'Doe_updated'


@pytest.mark.django_db
def test_only_logged_in_client_can_perform_update(client: django.test.Client, django_user_model):
    user = django_user_model.objects.create_user(
        username='testuser',
        first_name='John',
        last_name='Doe',
        password='mysecretpass'
    )
    user.save()

    response = client.get(f'/users/{user.id}/update/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/users/{user.id}/update/'

    update_form = {
        'username': 'testuser_updated',
        'first_name': 'John_updated',
        'last_name': 'Doe_updated',
        'password1': 'mysecretpass',
        'password2': 'mysecretpass',
    }
    response = client.post(f'/users/{user.id}/update/', update_form)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/users/{user.id}/update/'

    user.refresh_from_db()
    assert user.username == 'testuser'
    assert user.first_name == 'John'
    assert user.last_name == 'Doe'


@pytest.mark.django_db
def test_user_can_update_only_themselves(client: django.test.Client, django_user_model):
    self = django_user_model.objects.create_user(username='self', password='selfpassword')
    self.save()

    other_user = django_user_model.objects.create_user(
        username='testuser',
        first_name='John',
        last_name='Doe',
        password='mysecretpass'
    )
    other_user.save()

    logged_in = client.login(username=self.username, password='selfpassword')
    assert logged_in

    response = client.get(f'/users/{other_user.id}/update/')
    assert response.status_code == HTTPStatus.FORBIDDEN

    update_form = {
       'username': 'testuser_updated',
        'first_name': 'John_updated',
        'last_name': 'Doe_updated',
        'password1': 'mysecretpass',
        'password2': 'mysecretpass',
    }
    response = client.post(f'/users/{other_user.id}/update/', update_form)
    assert response.status_code == HTTPStatus.FORBIDDEN

    other_user.refresh_from_db()
    assert other_user.username == 'testuser'
    assert other_user.first_name == 'John'
    assert other_user.last_name == 'Doe'
