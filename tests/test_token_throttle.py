# tests/test_token_throttle.py
import pytest
from unittest.mock import patch
from users.views import CustomTokenObtainPairView
import sys
import importlib


def test_throttle_classes_in_production():
    """Test that throttle_classes is set correctly when not in pytest"""
    # Guardar el módulo original de users.views
    import users.views as original_views

    # 1. Parchear sys.argv ANTES de importar
    original_argv = sys.argv
    sys.argv = ["manage.py", "runserver"]  # Simular producción

    try:
        # 2. Recargar el módulo para que vea el sys.argv parcheado
        importlib.reload(original_views)

        # 3. Ahora crear la vista debería usar throttle_classes
        view = original_views.CustomTokenObtainPairView()
        assert (
            len(view.throttle_classes) == 1
        ), f"Expected 1 throttle class, got {view.throttle_classes}"
        assert view.throttle_classes[0].__name__ == "LoginRateThrottle"

    finally:
        # 4. Restaurar sys.argv y recargar el módulo original
        sys.argv = original_argv
        importlib.reload(original_views)


def test_throttle_classes_in_test():
    """Test that throttle_classes is empty during tests (current behavior)"""
    from users.views import CustomTokenObtainPairView

    view = CustomTokenObtainPairView()
    assert (
        view.throttle_classes == []
    ), f"Expected empty in tests, got {view.throttle_classes}"
