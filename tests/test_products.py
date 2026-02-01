import pytest
from factories import ProductFactory


@pytest.mark.django_db
def test_client_cannot_create_product(api_client, client_user, get_token):
    token = get_token(client_user)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = api_client.post(
        "/api/products/",
        {
            "name": "Producto Prohibido",
            "price": "100.00",
            "stock": 10,
            "is_public": True,
        },
        format="json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_staff_can_create_product(api_client, staff_user, get_token):
    token = get_token(staff_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = api_client.post(
        "/api/products/",
        {
            "name": "Producto Staff",
            "price": "50.00",
            "stock": 5,
            "is_public": True,
        },
        format="json",
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_staff_cannot_delete_product(api_client, staff_user, get_token):
    product = ProductFactory()

    token = get_token(staff_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = api_client.delete(f"/api/products/{product.id}/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_delete_product(api_client, admin_user, get_token):
    product = ProductFactory()

    token = get_token(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = api_client.delete(f"/api/products/{product.id}/")

    assert response.status_code == 204


@pytest.mark.django_db
def test_client_sees_only_own_products(api_client, client_user, get_token):
    ProductFactory.create_batch(3, owner=client_user)
    ProductFactory.create_batch(2)

    token = get_token(client_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = api_client.get("/api/products/")
    assert len(response.data) == 3


@pytest.mark.django_db
def test_staff_sees_only_public_products(api_client, staff_user, get_token):
    ProductFactory.create_batch(2, is_public=True)
    ProductFactory.create_batch(2, is_public=False)

    token = get_token(staff_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = api_client.get("/api/products/")
    assert len(response.data) == 2


@pytest.mark.django_db
def test_admin_sees_all_products(api_client, admin_user, get_token):
    ProductFactory.create_batch(5)

    token = get_token(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = api_client.get("/api/products/")
    assert len(response.data) == 5
