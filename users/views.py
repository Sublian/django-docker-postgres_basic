from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from .serializers import (
    UserSerializer, 
    UserCreateSerializer, 
    UserUpdateSerializer,
    LoginSerializer,
    ChangePasswordSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de usuarios
    """
    queryset = CustomUser.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        # Login y registro son públicos
        if self.action in ['create', 'login']:
            return [AllowAny()]
        # Todo lo demás requiere autenticación
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Registrar nuevo usuario"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'Usuario creado exitosamente',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """Listar todos los usuarios"""
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'users': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        """Obtener un usuario específico"""
        instance = self.get_object()
        serializer = UserSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Actualizar usuario completo"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Usuario actualizado exitosamente',
            'user': UserSerializer(instance).data
        })

    def destroy(self, request, *args, **kwargs):
        """Eliminar usuario"""
        instance = self.get_object()
        username = instance.username
        instance.delete()
        
        return Response({
            'message': f'Usuario {username} eliminado exitosamente'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Login de usuario"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user:
            login(request, user)
            return Response({
                'message': 'Login exitoso',
                'user': UserSerializer(user).data
            })
        
        return Response({
            'error': 'Credenciales inválidas'
        }, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout de usuario"""
        logout(request)
        return Response({
            'message': 'Logout exitoso'
        })

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener perfil del usuario actual"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Cambiar contraseña del usuario actual"""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Verificar contraseña actual
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'error': 'Contraseña actual incorrecta'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Cambiar contraseña
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Contraseña cambiada exitosamente'
        })