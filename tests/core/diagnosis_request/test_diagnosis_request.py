from typing import Callable

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import DiagnosisRequest, DiagnosisResult, User


@pytest.mark.django_db
def test_diagnosis_request_create(auth_client: APIClient, test_user: User, test_image: Callable) -> None:
    url = reverse('core:diagnosis_requests-list')

    response = auth_client.post(
        url,
        data={'image': test_image(), 'user': test_user.id},
        format='multipart',
    )

    assert response.status_code == 201, response.data

    diagnosis_request = DiagnosisRequest.objects.get(id=response.data['id'])
    assert diagnosis_request.user == test_user

    # Проверяем, что модель отработала и создала DiagnosisResult
    result = DiagnosisResult.objects.filter(request=diagnosis_request).first()
    assert result is not None

    # Проверяем, что модель вернула вероятности
    assert 0 <= result.confidence <= 100


@pytest.mark.django_db
def test_diagnosis_request_create_unauthorized(api_client: APIClient, test_image: Callable) -> None:
    """
    Неавторизованный пользователь НЕ может создать запрос диагностики.
    Ожидаем 401.
    """

    url = reverse('core:diagnosis_requests-list')

    response = api_client.post(
        url,
        data={'image': test_image()},
        format='multipart',
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_diagnosis_request_list_patient(auth_client: APIClient, test_user: User, test_image: Callable) -> None:
    url = reverse('core:diagnosis_requests-list')

    resp1 = auth_client.post(url, data={'image': test_image(), 'user': test_user.id}, format='multipart')
    resp2 = auth_client.post(url, data={'image': test_image(), 'user': test_user.id}, format='multipart')

    assert resp1.status_code == 201, resp1.data
    assert resp2.status_code == 201, resp2.data

    # Создаём чужой запрос
    other_user = User.objects.create_user('other', '12345678', role='patient')
    DiagnosisRequest.objects.create(user=other_user, image=test_image())

    list_response = auth_client.get(url)
    assert list_response.status_code == 200

    assert len(list_response.data) == 2
