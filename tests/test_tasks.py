import pytest
import django.test
from http import HTTPStatus

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


@pytest.mark.django_db
def test_get_tasks_fails_if_not_logged_in(client: django.test.Client):
    response = client.get('/tasks/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/?next=/tasks/'


@pytest.mark.django_db
def test_get_tasks(logged_in_client: django.test.Client):
    response = logged_in_client.get('/tasks/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_get_tasks_with_filters(logged_in_client: django.test.Client, make_test_user):
    status = Status(name='Open')
    status.save()

    executor, _ = make_test_user(username='exectuor')
    author, _ = make_test_user(username='author')

    label = Label(name='IT')
    label.save()

    task = Task(name='Task', author=author, executor=executor, status=status)
    task.save()
    task.labels.add(label)  # type: ignore
    task.save()

    response = logged_in_client.get(
        f'/tasks/?status={status.pk}&executor={executor.pk}&label={label.pk}&self_task=on')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_create_task_fails_if_not_logged_in(client: django.test.Client):
    response = client.get('/tasks/create/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/login/?next=/tasks/create/'


@pytest.mark.django_db
def test_create_task(logged_in_client: django.test.Client):
    response = logged_in_client.get('/tasks/create/')
    assert response.status_code == HTTPStatus.OK

    status = Status(name='Open')
    status.save()

    response = logged_in_client.post('/tasks/create/', data={
        'name': 'some task',
        'description': 'some task description',
        'status': status.pk,
    })
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/tasks/'


@pytest.mark.django_db
def test_create_task_fails_if_name_is_missing(logged_in_client: django.test.Client):
    status = Status(name='Open')
    status.save()

    response = logged_in_client.post('/tasks/create/', data={
        'description': 'some task description',
        'status': status.pk,
    })
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.django_db
def test_create_task_with_labels(logged_in_client: django.test.Client):
    response = logged_in_client.get('/tasks/create/')
    assert response.status_code == HTTPStatus.OK

    status = Status(name='Open')
    status.save()

    label_IT = Label(name='IT')
    label_IT.save()
    label_QA = Label(name='QA')
    label_QA.save()

    response = logged_in_client.post('/tasks/create/', data={
        'name': 'some task',
        'description': 'some task description',
        'status': status.pk,
        'labels': [
            label_IT.pk,
            label_QA.pk,
        ]
    })
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/tasks/'


@pytest.mark.django_db
def test_delete_task_fails_if_not_logged_in(client: django.test.Client, make_test_user):
    status = Status(name='Open')
    status.save()

    user, _ = make_test_user()
    task = Task(name='Some task', author=user, status=status)
    task.save()

    response = client.get(f'/tasks/{task.pk}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/tasks/{task.pk}/delete/'

    response = client.post(f'/tasks/{task.pk}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/tasks/{task.pk}/delete/'

    task.refresh_from_db()
    assert task.pk is not None


@pytest.mark.django_db
def test_delete_status(logged_in_client: django.test.Client, make_test_user):
    status = Status(name='Open')
    status.save()

    user, _ = make_test_user(username='author')
    task = Task(name='Some task', author=user, status=status)
    task.save()

    response = logged_in_client.get(f'/tasks/{task.pk}/delete/')
    assert response.status_code == HTTPStatus.OK

    response = logged_in_client.post(f'/tasks/{task.pk}/delete/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/tasks/'

    response = logged_in_client.get(f'/tasks/{task.pk}/delete/')
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_update_task_fails_if_not_logged_in(client: django.test.Client, make_test_user):
    status = Status(name='Open')
    status.save()

    user, _ = make_test_user(username='author')
    task = Task(name='Some task', author=user, status=status)
    task.save()

    response = client.get(f'/tasks/{task.pk}/update/')
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/tasks/{task.pk}/update/'

    response = client.post(f'/tasks/{task.pk}/update/', data={'name': 'New task'})
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'/login/?next=/tasks/{status.pk}/update/'

    task.refresh_from_db()
    assert task.name == 'Some task'


@pytest.mark.django_db
def test_update_task(logged_in_client: django.test.Client, make_test_user):
    status = Status(name='Open')
    status.save()

    user, _ = make_test_user(username='author')
    task = Task(name='Some task', author=user, status=status)
    task.save()

    response = logged_in_client.get(f'/tasks/{task.pk}/update/')
    assert response.status_code == HTTPStatus.OK

    new_status = Status(name='In Progress')
    new_status.save()

    executor, _ = make_test_user(username='executor')
    response = logged_in_client.post(f'/tasks/{task.pk}/update/', data={
        'name': 'New task',
        'description': 'New task description',
        'executor': executor.pk,
        'status': new_status.pk,
    })
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/tasks/'

    task.refresh_from_db()
    assert task.name == 'New task'
    assert task.description == 'New task description'
    assert task.executor == executor
    assert task.status == new_status


@pytest.mark.django_db
def test_update_task_with_labels(logged_in_client: django.test.Client, make_test_user):
    status = Status(name='Open')
    status.save()

    user, _ = make_test_user(username='author')
    task = Task(name='Some task', author=user, status=status)
    task.save()

    response = logged_in_client.get(f'/tasks/{task.pk}/update/')
    assert response.status_code == HTTPStatus.OK

    new_status = Status(name='In Progress')
    new_status.save()

    label_IT = Label(name='IT')
    label_IT.save()
    label_QA = Label(name='QA')
    label_QA.save()

    executor, _ = make_test_user(username='executor')
    response = logged_in_client.post(f'/tasks/{task.pk}/update/', data={
        'name': 'New task',
        'description': 'New task description',
        'executor': executor.pk,
        'status': new_status.pk,
        'labels': [
            label_IT.pk,
            label_QA.pk,
        ]
    })
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/tasks/'

    task.refresh_from_db()
    assert task.name == 'New task'
    assert task.description == 'New task description'
    assert task.executor == executor
    assert task.status == new_status

    assert task.labels is not None
    assert task.labels.count() == 2
    assert task.labels.get(pk=label_IT.pk) == label_IT
    assert task.labels.get(pk=label_QA.pk) == label_QA
