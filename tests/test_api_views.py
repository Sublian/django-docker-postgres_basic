# Crear tests/test_api_views.py
import pytest


@pytest.mark.django_db
def test_protected_view_requires_authentication(api_client):
    """Test that ProtectedTestView requires authentication"""
    response = api_client.get("/api/protected/")
    assert response.status_code == 401  # Unauthorized


@pytest.mark.django_db
def test_protected_view_with_authentication(api_client, client_user, get_token):
    """Test that ProtectedTestView works with authentication"""
    token = get_token(client_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = api_client.get("/api/protected/")
    assert response.status_code == 200
    assert "Acceso correcto" in response.data["message"]
