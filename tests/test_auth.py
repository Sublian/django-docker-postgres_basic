import pytest

@pytest.mark.django_db
def test_jwt_login_success(api_client, client_user):
    response = api_client.post(
        "/api/login/",
        {
            "username": client_user.username,
            "password": "123456"
        },
        format="json"
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_protected_without_token(api_client):
    response = api_client.get("/api/protected/")
    assert response.status_code == 401
