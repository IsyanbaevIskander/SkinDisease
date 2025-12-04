import pytest
from rest_framework.test import APIClient

from core.models import User

pytest_plugins = [
    'tests.core.diagnosis_request.fixtures',
]


@pytest.fixture
def test_user() -> User:
    return User.objects.create_user(username='test_user', password='12345678', role='patient')


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def auth_client(test_user: User) -> APIClient:
    client = APIClient()
    client.force_login(user=test_user)

    return client
