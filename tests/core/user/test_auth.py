import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import User


@pytest.mark.django_db
def test_jwt_token_obtain(api_client: APIClient, test_user: User) -> None:
    url = reverse('token_obtain_pair')

    response = api_client.post(url, {'username': test_user.username, 'password': '12345678'})

    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_jwt_token_obtain_wrong_password(api_client: APIClient, test_user: User) -> None:
    url = reverse('token_obtain_pair')

    response = api_client.post(url, {'username': test_user.username, 'password': 'wrong_password'})

    assert response.status_code == 401


@pytest.mark.django_db
def test_jwt_token_refresh(api_client: APIClient, test_user: User) -> None:
    # сначала получаем токены
    obtain_url = reverse('token_obtain_pair')
    refresh_url = reverse('token_refresh')

    obtain_response = api_client.post(obtain_url, {'username': test_user.username, 'password': '12345678'})

    assert obtain_response.status_code == 200
    refresh_token = obtain_response.data['refresh']

    # отправляем refresh
    refresh_response = api_client.post(refresh_url, {'refresh': refresh_token})

    assert refresh_response.status_code == 200


@pytest.mark.django_db
def test_jwt_token_refresh_invalid(api_client: APIClient) -> None:
    url = reverse('token_refresh')

    response = api_client.post(url, {'refresh': 'invalid.refresh.token'})

    assert response.status_code == 401
