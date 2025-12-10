import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.cache import cache
from factories import AdminFactory, StaffFactory, UserFactory

User = get_user_model()

@pytest.fixture(autouse=True)
def clear_throttle_cache():
    cache.clear()

@pytest.fixture(autouse=True)
def disable_throttling(settings):
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []
    
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return AdminFactory()


@pytest.fixture
def staff_user():
    return StaffFactory()


@pytest.fixture
def client_user():
    return UserFactory()


@pytest.fixture
def get_token(api_client):
    def _get_token(user):
        response = api_client.post(
            "/api/login/",
            {
                "username": user.username,
                "password": "123456"
            },
            format="json"
        )

        assert response.status_code == 200, f"Login failed: {response.status_code} - {response.data}"

        return response.data["access"]
    return _get_token
