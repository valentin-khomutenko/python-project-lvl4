import pytest
import django.test
from http import HTTPStatus

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


@pytest.mark.django_db
def test_get_labels_fails_if_not_logged_in(client: django.test.Client):
    response = client.get('/labels/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/?next=/labels/'


@pytest.mark.django_db
def test_get_labels(logged_in_client: django.test.Client):
    response = logged_in_client.get('/labels/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_create_label_fails_if_not_logged_in(client: django.test.Client):
    response = client.get('/labels/create/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/?next=/labels/create/'


@pytest.mark.django_db
def test_create_status(logged_in_client: django.test.Client):
    response = logged_in_client.get('/labels/create/')
    assert response.status_code == HTTPStatus.OK

    response = logged_in_client.post('/labels/create/', data={'name': 'IT'})
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/labels/'


@pytest.mark.django_db
def test_create_label_fails_if_name_is_not_unique(logged_in_client: django.test.Client):
    Label(name='IT').save()
    response = logged_in_client.post('/labels/create/', data={'name': 'IT'})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.django_db
def test_delete_label_fails_if_not_logged_in(client: django.test.Client):
    label = Label(name='IT')
    label.save()

    response = client.get(f'/labels/{label.pk}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/labels/{label.pk}/delete/'

    response = client.post(f'/labels/{label.pk}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/labels/{label.pk}/delete/'

    label.refresh_from_db()
    assert label.pk is not None


@pytest.mark.django_db
def test_delete_label_fails_if_in_use(logged_in_client: django.test.Client, make_test_user):
    label = Label(name='IT')
    label.save()

    user, _ = make_test_user(username='author')
    status = Status(name='Open')
    status.save()

    task = Task(name='task', author=user, status=status)
    task.save()
    task.labels.add(label)
    task.save()

    response = logged_in_client.get(f'/labels/{label.pk}/delete/')
    assert response.status_code == HTTPStatus.OK

    response = logged_in_client.post(f'/labels/{label.pk}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/labels/'

    response = logged_in_client.get(f'/labels/{label.pk}/delete/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_delete_label(logged_in_client: django.test.Client):
    label = Label(name='IT')
    label.save()

    response = logged_in_client.get(f'/labels/{label.pk}/delete/')
    assert response.status_code == HTTPStatus.OK

    response = logged_in_client.post(f'/labels/{label.pk}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/labels/'

    response = logged_in_client.get(f'/labels/{label.pk}/delete/')
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_update_label_fails_if_not_logged_in(client: django.test.Client):
    label = Label(name='IT')
    label.save()

    response = client.get(f'/labels/{label.pk}/update/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/labels/{label.pk}/update/'

    response = client.post(f'/labels/{label.pk}/update/', data={'name': 'IT department'})
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/labels/{label.pk}/update/'

    label.refresh_from_db()
    assert label.name == 'IT'


@pytest.mark.django_db
def test_update_label(logged_in_client: django.test.Client):
    label = Label(name='IT')
    label.save()

    response = logged_in_client.get(f'/labels/{label.pk}/update/')
    assert response.status_code == HTTPStatus.OK

    response = logged_in_client.post(f'/labels/{label.pk}/update/', data={'name': 'IT department'})
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/labels/'

    label.refresh_from_db()
    assert label.name == 'IT department'


@pytest.mark.django_db
def test_update_status_fails_if_name_is_not_unique(logged_in_client: django.test.Client):
    Label(name='IT').save()
    label = Label(name='QA')
    label.save()

    response = logged_in_client.post(f'/labels/{label.pk}/update/', data={'name': 'IT'})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
