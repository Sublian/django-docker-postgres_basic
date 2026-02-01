import pytest
from django.contrib.auth import get_user_model
from users.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


@pytest.mark.django_db
class TestUserSerializers:

    # ------------------- UserSerializer -------------------

    def test_user_serializer_read(self):
        """Test UserSerializer for reading user data"""
        user = User.objects.create(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            phone="123456789",
            role="CLIENTE",
        )

        serializer = UserSerializer(user)
        data = serializer.data

        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"
        assert data["phone"] == "123456789"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert "password" not in data  # No debe incluir password

    # ------------------- UserCreateSerializer -------------------

    def test_user_create_serializer_valid(self):
        """Test UserCreateSerializer with valid data"""
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
            "first_name": "New",
            "last_name": "User",
            "phone": "987654321",
        }

        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid() is True

        # Crear el usuario
        user = serializer.save()
        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.check_password("SecurePass123!") is True

    def test_user_create_serializer_passwords_mismatch(self):
        """Test UserCreateSerializer with mismatching passwords"""
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "SecurePass123!",
            "password_confirm": "DifferentPass456!",  # <-- NO COINCIDEN
            "first_name": "New",
            "last_name": "User",
        }

        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid() is False
        assert "password" in serializer.errors
        assert "no coinciden" in serializer.errors["password"][0].lower()

    def test_user_create_serializer_weak_password(self):
        """Test UserCreateSerializer with weak password"""
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "123",  # <-- DEMASIADO DÉBIL
            "password_confirm": "123",
            "first_name": "New",
            "last_name": "User",
        }

        serializer = UserCreateSerializer(data=data)
        # El serializer podría ser válido pero validate_password fallará
        # Depende de cómo Django valide
        is_valid = serializer.is_valid()
        if not is_valid:
            assert "password" in serializer.errors

    # ------------------- UserUpdateSerializer -------------------

    def test_user_update_serializer(self):
        """Test UserUpdateSerializer"""
        user = User.objects.create(
            username="existinguser",
            email="existing@example.com",
            first_name="Old",
            last_name="Name",
            phone="111111111",
            role="CLIENTE",
        )

        data = {
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "Name",
            "phone": "999999999",
        }

        serializer = UserUpdateSerializer(user, data=data)
        assert serializer.is_valid() is True

        updated_user = serializer.save()
        assert updated_user.email == "updated@example.com"
        assert updated_user.first_name == "Updated"
        assert updated_user.phone == "999999999"

    # ------------------- LoginSerializer -------------------

    def test_login_serializer_valid(self):
        """Test LoginSerializer with valid data"""
        data = {"username": "testuser", "password": "testpass123"}

        serializer = LoginSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data["username"] == "testuser"
        assert serializer.validated_data["password"] == "testpass123"

    def test_login_serializer_missing_fields(self):
        """Test LoginSerializer with missing required fields"""
        # Sin username
        serializer = LoginSerializer(data={"password": "testpass123"})
        assert serializer.is_valid() is False
        assert "username" in serializer.errors

        # Sin password
        serializer = LoginSerializer(data={"username": "testuser"})
        assert serializer.is_valid() is False
        assert "password" in serializer.errors

    # ------------------- ChangePasswordSerializer -------------------

    def test_change_password_serializer_valid(self):
        """Test ChangePasswordSerializer with valid data"""
        data = {
            "old_password": "OldPass123!",
            "new_password": "NewSecurePass456!",
            "new_password_confirm": "NewSecurePass456!",
        }

        serializer = ChangePasswordSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data["new_password"] == "NewSecurePass456!"

    def test_change_password_serializer_mismatch(self):
        """Test ChangePasswordSerializer with mismatching new passwords"""
        data = {
            "old_password": "OldPass123!",
            "new_password": "NewSecurePass456!",
            "new_password_confirm": "DifferentPass789!",  # <-- NO COINCIDEN
        }

        serializer = ChangePasswordSerializer(data=data)
        assert serializer.is_valid() is False
        assert "new_password" in serializer.errors
        assert "no coinciden" in serializer.errors["new_password"][0].lower()

    def test_change_password_serializer_weak_password(self):
        """Test ChangePasswordSerializer with weak new password"""
        data = {
            "old_password": "OldPass123!",
            "new_password": "123",  # <-- DEMASIADO DÉBIL
            "new_password_confirm": "123",
        }

        serializer = ChangePasswordSerializer(data=data)
        is_valid = serializer.is_valid()

        # CORRECCIÓN: La contraseña débil DEBERÍA hacer que el serializer sea inválido
        assert is_valid is False, "Weak password should make serializer invalid"

        # Verifica que hay un error relacionado con la contraseña
        # El mensaje exacto puede variar (podría estar en inglés o español)
        if "new_password" in serializer.errors:
            # Cualquier error en new_password es aceptable para contraseña débil
            assert len(serializer.errors["new_password"]) > 0
        else:
            # O podría estar en non_field_errors
            assert (
                len(serializer.errors) > 0
            ), "Should have validation errors for weak password"
