import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import User


@pytest.mark.django_db
def test_user_list(auth_client: APIClient, test_user: User) -> None:
    url = reverse('core:users-list')

    response = auth_client.get(url)

    assert response.status_code == 200
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_user_list_unauthorized(api_client: APIClient) -> None:
    url = reverse('core:users-list')

    response = api_client.get(url)

    assert response.status_code == 401
    assert 'detail' in response.data


@pytest.mark.django_db
def test_user_retrieve(auth_client: APIClient, test_user: User) -> None:
    url = reverse('core:users-detail', args=[test_user.id])

    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.data['username'] == test_user.username


@pytest.mark.django_db
def test_user_create(auth_client: APIClient) -> None:
    url = reverse('core:users-list')

    payload = {
        'username': 'new_user',
        'password': '12345678',
        'role': 'patient',
        'first_name': 'Test',
        'last_name': 'Test',
    }

    response = auth_client.post(url, payload)

    assert response.status_code == 201
    data = response.data

    assert data['username'] == 'new_user'
    assert 'password' not in data
    assert User.objects.filter(username='new_user').exists()


@pytest.mark.django_db
def test_user_partial_update(auth_client: APIClient, test_user: User) -> None:
    url = reverse('core:users-detail', args=[test_user.id])

    payload = {
        'first_name': 'UpdatedName',
        'role': 'dermatologist',
    }

    response = auth_client.patch(url, payload)

    assert response.status_code == 200

    test_user.refresh_from_db()
    assert test_user.first_name == 'UpdatedName'
    assert test_user.role == 'dermatologist'


@pytest.mark.django_db
def test_user_delete(auth_client: APIClient, test_user: User) -> None:
    url = reverse('core:users-detail', args=[test_user.id])

    response = auth_client.delete(url)

    assert response.status_code == 204
    assert not User.objects.filter(id=test_user.id).exists()
