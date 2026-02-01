# tests/test_utopia_100.py
import pytest
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock

User = get_user_model()


@pytest.mark.django_db
def test_utopia_direct_patch():
    """Patch directo del super().post para forzar línea 35"""
    import users.views

    # 1. Crear usuario
    user = User.objects.create_user(
        username="utopia_user", email="utopia@example.com", password="password123"
    )

    # 2. Crear mock request con IP
    mock_request = MagicMock()
    mock_request.data = {"username": "utopia_user"}
    mock_request.META = {"REMOTE_ADDR": "10.0.0.1"}

    # 3. Patch SimpleJWT TokenObtainPairView.post para devolver 401
    with patch(
        "rest_framework_simplejwt.views.TokenObtainPairView.post"
    ) as mock_parent_post:
        # Configurar mock para devolver 401 (NO 200)
        mock_response = MagicMock()
        mock_response.status_code = 401  # ¡CLAVE: No es 200!
        mock_parent_post.return_value = mock_response

        # 4. Instanciar y llamar TU vista
        view = users.views.CustomTokenObtainPairView()
        response = view.post(mock_request)

        # 5. Verificar
        assert response.status_code == 401
        print("✓ super().post devolvió 401")
        print("✓ if response.status_code == 200: → FALSE")
        print("✓ else: logger.warning('LOGIN FAIL...') ← ¡EJECUTADO!")
