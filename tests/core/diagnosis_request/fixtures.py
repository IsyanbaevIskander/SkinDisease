from typing import Callable

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def test_image() -> Callable:
    def _make() -> SimpleUploadedFile:
        with open('tests/core/diagnosis_request/lichen.jpeg', 'rb') as f:
            return SimpleUploadedFile('img.jpeg', f.read(), content_type='image/jpeg')

    return _make
