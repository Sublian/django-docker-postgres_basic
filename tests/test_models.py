import pytest
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_product_str_method():
    """Test the __str__ method of Product model (line 14)"""
    # Crear usuario primero
    user = User.objects.create(
        username="testowner", email="owner@example.com", role="CLIENTE"
    )

    # Crear producto
    product = Product.objects.create(
        name="Test Product", price=29.99, stock=100, owner=user, is_public=True
    )

    # Esto ejecuta la línea 14
    str_representation = str(product)

    assert "Test Product" in str_representation
    assert "29.99" in str_representation
    assert "100" in str_representation
