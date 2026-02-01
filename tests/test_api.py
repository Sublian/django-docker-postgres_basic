import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUserAPI:
    """Tests for users/api.py"""

    def test_login_with_invalid_credentials(self, api_client):
        """Test login with wrong credentials returns 400"""
        response = api_client.post(
            "/api/login/",
            {"username": "nonexistent", "password": "wrongpassword"},
            format="json",
        )

        # Should return 400 (Bad Request) or 401 (Unauthorized)
        assert response.status_code in [
            400,
            401,
        ], f"Expected 400/401, got {response.status_code}"
        assert "error" in response.data or "detail" in response.data

    def test_login_without_credentials(self, api_client):
        """Test login without required fields"""
        response = api_client.post("/api/login/", {}, format="json")

        # Should return 400 with validation errors
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert "username" in response.data or "password" in response.data
