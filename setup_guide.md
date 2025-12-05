# 🐳 Proyecto Django + PostgreSQL con Docker - Guía Completa

## 📁 Estructura Final del Proyecto

```
proyecto-django-docker/
├── docker-compose.yml          # Orquestación de contenedores
├── Dockerfile                  # Imagen de Django
├── requirements.txt            # Dependencias Python
├── .dockerignore              # Archivos a ignorar
├── .env                       # Variables de entorno (opcional)
├── init.sh                    # Script de inicialización
├── manage.py                  # Django management
├── myproject/                 # Configuración Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── users/                     # App de usuarios
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── urls.py
    ├── views.py
    └── migrations/
```

---

## 💻 REQUISITOS PREVIOS (Windows)

### Verificar Docker Desktop

1. **Docker Desktop instalado y corriendo**
   - Abre Docker Desktop
   - Verifica que el ícono de Docker en la barra de tareas esté activo (ballena)
   - Si dice "Docker Desktop is starting..." espera a que termine

2. **Verificar instalación en PowerShell o CMD**
```powershell
docker --version
docker-compose --version
```

Deberías ver algo como:
```
Docker version 24.0.x
Docker Compose version v2.x.x
```

3. **Configuración recomendada en Docker Desktop**
   - Settings → Resources → Asigna al menos 4GB de RAM
   - Settings → General → Activa "Use WSL 2 based engine" (recomendado)
   - Settings → Docker Engine → Deja la configuración por defecto

### Editor de texto recomendado
- **Visual Studio Code** con extensiones:
  - Docker (Microsoft)
  - Python (Microsoft)
  - Remote - Containers (Microsoft)

---

## 🚀 PASO 1: Crear estructura y archivos base

### 1.1 Crear directorio del proyecto

**En PowerShell o CMD:**
```powershell
mkdir proyecto-django-docker
cd proyecto-django-docker
```

**O usando el Explorador de Windows:**
- Crea una carpeta llamada `proyecto-django-docker` en tu ubicación preferida
- Abre esa carpeta en VS Code: `File → Open Folder`
- Abre la terminal integrada: `Terminal → New Terminal` (Ctrl + Ñ)

### 1.2 Crear `requirements.txt`
```txt
Django==4.2.7
psycopg2-binary==2.9.9
djangorestframework==3.14.0
```

### 1.3 Crear `Dockerfile`
```dockerfile
FROM python:3.11-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de dependencias
COPY requirements.txt /app/

# Actualizar pip e instalar dependencias Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . /app/

# Exponer puerto 8000
EXPOSE 8000

# Comando por defecto (se sobrescribe en docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 1.4 Crear `.dockerignore`
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
*.sqlite3
db.sqlite3
*.db
.DS_Store
*.swp
*.swo
*~
.idea/
.vscode/
```

### 1.5 Crear `docker-compose.yml`
```yaml
version: '3.8'

services:
  # Servicio de Base de Datos PostgreSQL
  db:
    image: postgres:15-alpine
    container_name: django_postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: django_db
      POSTGRES_USER: django_user
      POSTGRES_PASSWORD: django_pass
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U django_user -d django_db"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - django_network

  # Servicio de Django
  web:
    build: .
    container_name: django_web
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      DB_NAME: django_db
      DB_USER: django_user
      DB_PASSWORD: django_pass
      DB_HOST: db
      DB_PORT: 5432
      DJANGO_SETTINGS_MODULE: myproject.settings
    depends_on:
      db:
        condition: service_healthy
    networks:
      - django_network

volumes:
  postgres_data:

networks:
  django_network:
    driver: bridge
```

### 1.6 Crear script de inicialización

**⚠️ IMPORTANTE para Windows:**

En Windows, en lugar del script `init.sh` (que es para Linux/Mac), usaremos un archivo `.bat` o ejecutaremos los comandos directamente.

**Opción 1: Crear `init.bat` (Windows)**
```batch
@echo off
echo Iniciando proyecto Django con Docker...

echo Construyendo imagenes Docker...
docker-compose build

echo Verificando si manage.py existe...
if not exist "manage.py" (
    echo Creando proyecto Django...
    docker-compose run --rm web django-admin startproject myproject .
) else (
    echo Proyecto Django ya existe
)

echo Verificando si app users existe...
if not exist "users\" (
    echo Creando app de usuarios...
    docker-compose run --rm web python manage.py startapp users
) else (
    echo App users ya existe
)

echo.
echo Estructura base creada!
echo.
echo Proximos pasos:
echo 1. Configura settings.py segun la guia
echo 2. Crea los modelos, serializers y vistas
echo 3. Ejecuta: docker-compose up
pause
```

**Opción 2: Ejecutar comandos manualmente (Recomendado para empezar)**

En PowerShell o CMD, ejecuta uno por uno:
```powershell
# Construir imágenes
docker-compose build

# Crear proyecto Django (solo primera vez)
docker-compose run --rm web django-admin startproject myproject .

# Crear app users (solo primera vez)
docker-compose run --rm web python manage.py startapp users
```

---

## 🔧 PASO 2: Inicializar el proyecto

**En PowerShell, CMD o terminal de VS Code:**

```powershell
# Construir imágenes (esto instala las dependencias de requirements.txt)
docker-compose build

# Crear proyecto Django (solo primera vez)
docker-compose run --rm web django-admin startproject myproject .

# Crear app users (solo primera vez)
docker-compose run --rm web python manage.py startapp users
```

**⚠️ Nota importante sobre permisos en Windows:**
- Los archivos creados por Docker pueden tener permisos diferentes
- Si no puedes editarlos, cierra VS Code y vuelve a abrir la carpeta
- Alternativamente, puedes crear los archivos manualmente y copiar el contenido

**💡 Tip:** Si usas Git Bash en Windows, puedes usar los comandos de Linux/Mac también.

---

## ⚙️ PASO 3: Configurar Django

### 3.1 Editar `myproject/settings.py`

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-cambiar-en-produccion'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'rest_framework',
    # Apps locales
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# 🔥 CONFIGURACIÓN DE BASE DE DATOS POSTGRESQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'django_db'),
        'USER': os.environ.get('DB_USER', 'django_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'django_pass'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🔥 MODELO DE USUARIO PERSONALIZADO
AUTH_USER_MODEL = 'users.CustomUser'

# 🔥 CONFIGURACIÓN DE REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### 3.2 Crear modelo en `users/models.py`

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado con campos adicionales
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return self.username
```

### 3.3 Crear `users/serializers.py`

```python
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """Serializer para lectura de usuarios"""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'first_name', 
                  'last_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para creación de usuarios"""
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm', 
                  'phone', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Las contraseñas no coinciden"
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualización de usuarios"""
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'first_name', 'last_name']

class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, 
        write_only=True,
        style={'input_type': 'password'}
    )

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambio de contraseña"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True, 
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password": "Las contraseñas no coinciden"
            })
        return attrs
```

### 3.4 Crear `users/views.py`

```python
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
```

### 3.5 Crear `users/urls.py`

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
```

### 3.6 Editar `myproject/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
]
```

### 3.7 Configurar admin en `users/admin.py`

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', 'is_staff', 'is_active', 'created_at']
    list_filter = ['is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'phone']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('phone', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
```

---

## 🎯 PASO 4: Ejecutar el proyecto

### 4.1 Aplicar migraciones

**En PowerShell/CMD:**
```powershell
docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate
```

### 4.2 Crear superusuario

```powershell
docker-compose run --rm web python manage.py createsuperuser
```

Te pedirá:
- Username
- Email
- Password (no se verá mientras escribes)
- Password confirmation

### 4.3 Iniciar servicios

**Modo normal (verás los logs en tiempo real):**
```powershell
docker-compose up
```

**Modo detached (segundo plano):**
```powershell
docker-compose up -d
```

**Para detener:**
- Modo normal: `Ctrl + C` en la terminal
- Modo detached: `docker-compose down`

### 4.4 Verificar que todo funciona

Abre tu navegador en:
- **API**: http://localhost:8000/api/users/
- **Admin**: http://localhost:8000/admin/

**💡 Tip Windows:** Si no carga, verifica:
1. Docker Desktop está corriendo
2. Los contenedores están activos: `docker-compose ps`
3. Firewall de Windows no está bloqueando el puerto 8000

---

## 🧪 PASO 5: Probar la API

### Opción 1: Usar el navegador (más fácil para Windows)

1. **Ver la interfaz de Django REST Framework**
   - Abre: http://localhost:8000/api/users/
   - Verás una interfaz web donde puedes hacer las peticiones

2. **Crear usuario desde el navegador**
   - Ve a: http://localhost:8000/api/users/
   - Completa el formulario en la parte inferior
   - Click en "POST"

3. **Login desde el navegador**
   - Ve a: http://localhost:8000/api/users/login/
   - Ingresa username y password
   - Click en "POST"

### Opción 2: Usar PowerShell con `curl`

**⚠️ Nota para Windows:** 
- PowerShell tiene su propio `Invoke-WebRequest` (alias `curl`)
- O puedes instalar curl real desde: https://curl.se/windows/
- O usar **Postman** (recomendado para principiantes)

**Con PowerShell nativo:**

### Crear usuario (Registro)
```powershell
$body = @{
    username = "juanperez"
    email = "juan@example.com"
    password = "MiPassword123!"
    password_confirm = "MiPassword123!"
    phone = "+51999888777"
    first_name = "Juan"
    last_name = "Pérez"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/users/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Login
```powershell
$body = @{
    username = "juanperez"
    password = "MiPassword123!"
} | ConvertTo-Json

$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession

Invoke-WebRequest -Uri "http://localhost:8000/api/users/login/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body `
    -SessionVariable session
```

### Opción 3: Usar Postman (RECOMENDADO para Windows)

1. **Descargar Postman**: https://www.postman.com/downloads/
2. **Crear una colección** llamada "Django Users API"
3. **Configurar requests:**

**POST - Crear usuario**
- URL: `http://localhost:8000/api/users/`
- Method: POST
- Body → raw → JSON:
```json
{
    "username": "juanperez",
    "email": "juan@example.com",
    "password": "MiPassword123!",
    "password_confirm": "MiPassword123!",
    "phone": "+51999888777",
    "first_name": "Juan",
    "last_name": "Pérez"
}
```

**POST - Login**
- URL: `http://localhost:8000/api/users/login/`
- Method: POST
- Body → raw → JSON:
```json
{
    "username": "juanperez",
    "password": "MiPassword123!"
}
```
- Ir a Tests y agregar (para guardar la sesión):
```javascript
pm.cookies.jar();
```

**GET - Ver perfil**
- URL: `http://localhost:8000/api/users/me/`
- Method: GET
- (Debe estar en la misma sesión después del login)

### Opción 4: Con curl real en Windows

Si instalaste curl de https://curl.se/windows/:

```bash
# Crear usuario
curl -X POST http://localhost:8000/api/users/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"juanperez\",\"email\":\"juan@example.com\",\"password\":\"MiPassword123!\",\"password_confirm\":\"MiPassword123!\",\"phone\":\"+51999888777\",\"first_name\":\"Juan\",\"last_name\":\"Perez\"}"

# Login (guarda cookies)
curl -X POST http://localhost:8000/api/users/login/ ^
  -H "Content-Type: application/json" ^
  -c cookies.txt ^
  -d "{\"username\":\"juanperez\",\"password\":\"MiPassword123!\"}"

# Ver perfil
curl -X GET http://localhost:8000/api/users/me/ ^
  -b cookies.txt
```

**Nota:** En CMD de Windows usa `^` en lugar de `\` para continuar líneas.

---

## 🐳 Comandos Docker Esenciales (Windows)

**En PowerShell, CMD o terminal de VS Code:**

```powershell
# Ver contenedores activos
docker-compose ps

# Ver TODOS los contenedores (incluso detenidos)
docker ps -a

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs solo de Django
docker-compose logs -f web

# Ver logs solo de PostgreSQL
docker-compose logs -f db

# Detener servicios (mantiene los datos)
docker-compose down

# Detener y eliminar volúmenes (⚠️ BORRA LA BASE DE DATOS)
docker-compose down -v

# Reiniciar servicios
docker-compose restart

# Reiniciar solo Django
docker-compose restart web

# Reconstruir imágenes (cuando cambias Dockerfile o requirements.txt)
docker-compose build --no-cache

# Ejecutar comandos en contenedor corriendo
docker-compose exec web python manage.py shell

# Acceder a bash del contenedor (para explorar)
docker-compose exec web bash
# O si bash no está disponible:
docker-compose exec web sh

# Conectar a PostgreSQL
docker-compose exec db psql -U django_user -d django_db

# Ver volúmenes creados
docker volume ls

# Ver imágenes descargadas
docker images

# Limpiar todo lo que no se usa (libera espacio)
docker system prune -a

# Ver uso de espacio en disco
docker system df
```

### 🔍 Comandos útiles para debugging en Windows

```powershell
# Ver estadísticas de recursos (CPU, RAM)
docker stats

# Inspeccionar un contenedor
docker inspect proyecto-django-docker-web-1

# Ver red creada
docker network ls
docker network inspect proyecto-django-docker_django_network

# Copiar archivo desde el contenedor a Windows
docker cp proyecto-django-docker-web-1:/app/manage.py ./manage_backup.py

# Copiar archivo desde Windows al contenedor
docker cp ./archivo.txt proyecto-django-docker-web-1:/app/
```

### 🛑 Detener Docker Desktop completamente

Si necesitas liberar recursos:
1. Click derecho en el ícono de Docker Desktop (ballena) en la bandeja
2. Selecciona "Quit Docker Desktop"
3. Para reiniciar, abre Docker Desktop desde el menú de inicio

---

## 📊 Endpoints Disponibles

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/users/` | Crear usuario | ❌ |
| GET | `/api/users/` | Listar usuarios | ✅ |
| GET | `/api/users/{id}/` | Ver usuario | ✅ |
| PUT | `/api/users/{id}/` | Actualizar (completo) | ✅ |
| PATCH | `/api/users/{id}/` | Actualizar (parcial) | ✅ |
| DELETE | `/api/users/{id}/` | Eliminar usuario | ✅ |
| POST | `/api/users/login/` | Login | ❌ |
| POST | `/api/users/logout/` | Logout | ✅ |
| GET | `/api/users/me/` | Perfil actual | ✅ |
| POST | `/api/users/change_password/` | Cambiar contraseña | ✅ |

---

## 🎓 Conceptos Docker para Junior (Explicación Windows)

### 1. **¿Por qué no necesito virtualenv?**

**Entorno tradicional (sin Docker):**
```
Windows → Python global → venv → Django
```
Problema: Cada proyecto contamina tu Windows con dependencias

**Con Docker:**
```
Windows → Docker Desktop → Contenedor aislado → Python + Django
```
✅ Cada contenedor es un "mini-ordenador" aislado
✅ No ensucias tu Windows
✅ Mismo ambiente en todos lados (Windows, Mac, Linux)

### 2. **Dockerfile - La "receta"**
```dockerfile
FROM python:3.11-slim          # Sistema base (como instalar Ubuntu)
WORKDIR /app                   # Carpeta de trabajo
COPY requirements.txt /app/    # Copiar lista de dependencias
RUN pip install -r requirements.txt  # Instalar dependencias
COPY . /app/                   # Copiar todo el código
```
👉 Es como un "script de instalación" que crea una **imagen** (plantilla)

### 3. **Imagen vs Contenedor**
- **Imagen**: plantilla inmutable (como un .exe instalador)
- **Contenedor**: instancia corriendo (como un programa abierto)

```powershell
docker-compose build  # Crea la IMAGEN
docker-compose up     # Crea y ejecuta CONTENEDORES desde la imagen
```

### 4. **docker-compose.yml - El orquestador**
Coordina múltiples contenedores:
```yaml
services:
  db:    # Contenedor 1: PostgreSQL
  web:   # Contenedor 2: Django
```
👉 Ambos corren simultáneamente y se comunican por red interna

### 5. **Volúmenes - Persistencia de datos**

**Tipos:**

a) **Volumen named** (para la base de datos):
```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```
👉 Datos persisten aunque borres el contenedor
👉 Docker los guarda en: `C:\Users\TuUsuario\AppData\Local\Docker\wsl\data\`

b) **Bind mount** (para código en desarrollo):
```yaml
volumes:
  - .:/app
```
👉 Tu carpeta de Windows se "monta" dentro del contenedor
👉 Cambios en Windows = cambios en el contenedor (hot reload)

### 6. **Redes - Comunicación entre contenedores**

En Windows, verías:
- Django: `localhost:8000`
- PostgreSQL: `localhost:5432`

Dentro de Docker:
- Django se conecta a: `db:5432` (nombre del servicio, no localhost)
- Docker crea una red privada entre contenedores

### 7. **Variables de Entorno**
```yaml
environment:
  DB_HOST: db      # Django lee esto en settings.py
  DB_USER: django_user
```
👉 Configuración sin hardcodear valores
👉 Diferente por ambiente (desarrollo, producción)

### 8. **Healthcheck - Espera inteligente**
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U django_user"]
```
👉 Django espera a que PostgreSQL esté listo
👉 Evita errores de "connection refused"

### 9. **Capas de Docker (layer caching)**

Dockerfile ejecuta comandos en orden:
```dockerfile
COPY requirements.txt /app/    # Capa 1 (cambia poco)
RUN pip install -r requirements.txt  # Capa 2 (se cachea)
COPY . /app/                   # Capa 3 (cambia mucho)
```
👉 Si solo cambias código, Docker reutiliza capas 1-2 (build rápido)
👉 Si cambias requirements.txt, reconstruye desde capa 2

### 10. **Modos de ejecución**

**Foreground (normal):**
```powershell
docker-compose up
```
👉 Ves logs en tiempo real
👉 Ctrl+C para detener

**Detached (background):**
```powershell
docker-compose up -d
```
👉 Corre en segundo plano
👉 Puedes cerrar la terminal

### 📊 Flujo completo visualizado

```
1. Escribes Dockerfile y docker-compose.yml
   ↓
2. docker-compose build
   → Descarga imagen base Python
   → Instala dependencias
   → Crea IMAGEN local
   ↓
3. docker-compose up
   → Crea red interna
   → Inicia contenedor PostgreSQL
   → Espera healthcheck
   → Inicia contenedor Django
   → Conecta ambos por red
   ↓
4. Accedes desde Windows:
   → localhost:8000 (puerto mapeado)
   → El resto es magia de Docker 🎩✨
```

### 🆚 Comparación: Sin Docker vs Con Docker

**Sin Docker en Windows:**
```powershell
# Instalar Python
# Crear venv
python -m venv venv
.\venv\Scripts\activate
# Instalar PostgreSQL nativo en Windows
# Configurar PostgreSQL
# Instalar dependencias
pip install -r requirements.txt
# Configurar variables de entorno
# Ejecutar
python manage.py runserver
```
❌ Muchos pasos
❌ Puede fallar en cada paso
❌ Diferente en Mac/Linux

**Con Docker en Windows:**
```powershell
docker-compose up
```
✅ Un comando
✅ Funciona siempre igual
✅ Mismo comando en Mac/Linux/Windows

### 🎯 Lo que Docker te resuelve

1. **"Funciona en mi máquina"** → Funciona en todas
2. **Dependencias conflictivas** → Cada proyecto aislado
3. **Instalar PostgreSQL** → Ya viene en el contenedor
4. **Configurar Python** → Ya viene configurado
5. **Compartir proyecto** → Solo necesitas Docker
6. **Cambiar de PC** → Llevas el proyecto completo

---

## 🌐 Accesos

- **Django Dev Server**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/users/
- **PostgreSQL**: localhost:5432
  - User: `django_user`
  - Pass: `django_pass`
  - Database: `django_db`

### 🔌 Conectar a PostgreSQL desde Windows

**Opción 1: pgAdmin (Interfaz gráfica)**
1. Descargar: https://www.pgadmin.org/download/pgadmin-4-windows/
2. Crear nuevo servidor:
   - Host: `localhost`
   - Port: `5432`
   - Database: `django_db`
   - Username: `django_user`
   - Password: `django_pass`

**Opción 2: DBeaver (Universal)**
1. Descargar: https://dbeaver.io/download/
2. New Connection → PostgreSQL
3. Usa las mismas credenciales

**Opción 3: VS Code**
1. Instala extensión: "PostgreSQL" de Chris Kolkman
2. Conecta con las credenciales de arriba

**Opción 4: Desde Docker (línea de comandos)**
```powershell
docker-compose exec db psql -U django_user -d django_db
```

Comandos útiles en psql:
```sql
-- Ver todas las tablas
\dt

-- Describir tabla users
\d users_customuser

-- Ver usuarios
SELECT * FROM users_customuser;

-- Salir
\q
```

---

## 🔧 Troubleshooting (Problemas comunes en Windows)

### ❌ "docker-compose: command not found"
**Solución:**
- Verifica que Docker Desktop esté corriendo
- En PowerShell, usa `docker compose` (sin guión) si tienes Docker Desktop v2+
- Reinicia la terminal después de instalar Docker

### ❌ Puerto 8000 ocupado
**Ver qué usa el puerto en Windows:**
```powershell
netstat -ano | findstr :8000
```

**Cambiar puerto en `docker-compose.yml`:**
```yaml
ports:
  - "8001:8000"  # Usa 8001 en lugar de 8000
```

### ❌ "Error: Database connection failed"
**Soluciones:**
1. Espera 10-15 segundos después de `docker-compose up`
2. Verifica que el contenedor de PostgreSQL esté healthy:
```powershell
docker-compose ps
```
3. Revisa logs de la base de datos:
```powershell
docker-compose logs db
```

### ❌ "Permission denied" al crear archivos
**Causa:** Docker en Windows crea archivos con permisos diferentes

**Soluciones:**
1. Ejecuta VS Code como administrador
2. O crea los archivos manualmente en Windows y copia el contenido
3. O cambia permisos:
```powershell
icacls "users" /grant Everyone:F /T
```

### ❌ "Drive has not been shared" (WSL 2)
**Solución:**
1. Docker Desktop → Settings → Resources → File Sharing
2. Agrega la unidad donde está tu proyecto (C:\, D:\, etc.)
3. Click "Apply & Restart"

### ❌ Contenedores muy lentos en Windows
**Soluciones:**
1. Usa WSL 2 en lugar de Hyper-V:
   - Docker Desktop → Settings → General
   - Activa "Use WSL 2 based engine"
2. Coloca el proyecto en WSL filesystem (mejor rendimiento):
   - Abre WSL: `wsl`
   - Crea proyecto en `/home/tuusuario/proyectos/`
3. Aumenta recursos:
   - Docker Desktop → Settings → Resources
   - Asigna más CPU y RAM

### ❌ "No space left on device"
**Limpiar Docker:**
```powershell
# Ver espacio usado
docker system df

# Limpiar contenedores, imágenes y redes no usadas
docker system prune -a

# Limpiar volúmenes no usados (⚠️ cuidado)
docker volume prune
```

### ❌ Hot reload no funciona (cambios no se reflejan)
**Causa:** Sincronización de archivos entre Windows y Docker

**Soluciones:**
1. Reinicia el contenedor:
```powershell
docker-compose restart web
```
2. Si persiste, detén y vuelve a levantar:
```powershell
docker-compose down
docker-compose up
```
3. Usa polling en Django (más lento pero funciona):
```bash
python manage.py runserver 0.0.0.0:8000 --noreload
```

### ❌ Firewall de Windows bloquea puertos
**Solución:**
1. Windows Security → Firewall & network protection
2. Allow an app through firewall
3. Busca "Docker Desktop" y permite redes privadas/públicas

### ❌ "Cannot connect to Docker daemon"
**Soluciones:**
1. Verifica que Docker Desktop esté corriendo (ícono de ballena)
2. Si está "starting", espera a que termine
3. Reinicia Docker Desktop:
   - Click derecho → Restart
4. Si persiste, reinicia Windows

### 🔄 Reconstruir todo desde cero (solución definitiva)

```powershell
# 1. Detener y eliminar todo
docker-compose down -v

# 2. Eliminar imágenes del proyecto
docker rmi proyecto-django-docker-web

# 3. Limpiar todo Docker (opcional)
docker system prune -a

# 4. Reconstruir sin caché
docker-compose build --no-cache

# 5. Levantar servicios
docker-compose up
```

### 📱 Ver logs en Docker Desktop (interfaz gráfica)

1. Abre Docker Desktop
2. Ve a "Containers" en el menú lateral
3. Click en tu proyecto (`proyecto-django-docker`)
4. Verás los logs de todos los contenedores con colores
5. Puedes pausar, reiniciar o detener desde ahí

---

## ✅ Checklist de verificación (Windows)

### Antes de empezar:
- [ ] Docker Desktop instalado y corriendo (ícono ballena activo)
- [ ] Terminal abierta (PowerShell, CMD o VS Code)
- [ ] Editor de texto (VS Code recomendado)

### Configuración inicial:
- [ ] Carpeta `proyecto-django-docker` creada
- [ ] `Dockerfile` creado
- [ ] `docker-compose.yml` creado
- [ ] `requirements.txt` creado
- [ ] `.dockerignore` creado

### Build y setup:
- [ ] `docker-compose build` ejecutado exitosamente
- [ ] Proyecto Django creado con `django-admin startproject`
- [ ] App `users` creada con `startapp`
- [ ] `settings.py` configurado (DATABASES, INSTALLED_APPS, AUTH_USER_MODEL)
- [ ] Modelos creados en `users/models.py`
- [ ] Serializers creados en `users/serializers.py`
- [ ] Views creados en `users/views.py`
- [ ] URLs configuradas (`users/urls.py` y `myproject/urls.py`)
- [ ] Admin registrado en `users/admin.py`

### Migraciones y datos:
- [ ] `makemigrations` ejecutado sin errores
- [ ] `migrate` ejecutado sin errores
- [ ] Superusuario creado con `createsuperuser`

### Servicios corriendo:
- [ ] `docker-compose up` levantó ambos servicios
- [ ] `docker-compose ps` muestra contenedores "Up"
- [ ] http://localhost:8000 responde (puede dar error 404, está bien)
- [ ] http://localhost:8000/admin/ muestra login
- [ ] http://localhost:8000/api/users/ muestra interfaz DRF

### Pruebas funcionales:
- [ ] Puedes crear usuario desde http://localhost:8000/api/users/
- [ ] Puedes hacer login desde http://localhost:8000/api/users/login/
- [ ] Puedes ver tu perfil en http://localhost:8000/api/users/me/
- [ ] Admin panel funciona con tu superusuario

### Docker funcionando:
- [ ] `docker-compose logs` no muestra errores críticos
- [ ] PostgreSQL healthcheck está "healthy"
- [ ] Puedes detener con `docker-compose down`
- [ ] Puedes volver a levantar con `docker-compose up`

**¡Proyecto completo funcionando en Windows!** 🎉🪟

---

## 🚀 Mejoras futuras (para seguir aprendiendo)

Una vez que domines este proyecto básico, puedes agregar:

### Nivel intermedio:
- [ ] Agregar `docker-compose.prod.yml` para producción
- [ ] Usar variables `.env` en lugar de hardcodear en docker-compose
- [ ] Agregar Nginx como reverse proxy
- [ ] Implementar JWT tokens en lugar de sesiones
- [ ] Agregar Redis para caché
- [ ] Usar Gunicorn en lugar de runserver

### Nivel avanzado:
- [ ] CI/CD con GitHub Actions
- [ ] Deploy en AWS/Azure/DigitalOcean
- [ ] Monitoreo con Prometheus + Grafana
- [ ] Logging centralizado con ELK Stack
- [ ] Implementar tests automatizados
- [ ] Multi-stage builds en Dockerfile

---

## 📚 Recursos adicionales para Windows + Docker

### Documentación oficial:
- Docker Desktop para Windows: https://docs.docker.com/desktop/windows/
- Docker Compose: https://docs.docker.com/compose/
- Django: https://docs.djangoproject.com/

### Tutoriales recomendados:
- Docker para principiantes (español): https://www.youtube.com/results?search_query=docker+tutorial+español
- Django REST Framework: https://www.django-rest-framework.org/tutorial/quickstart/

### Herramientas útiles:
- **Postman**: Para probar APIs (https://www.postman.com/)
- **pgAdmin**: Interfaz gráfica para PostgreSQL
- **Docker Extension para VS Code**: Gestión visual de contenedores
- **WSL 2**: Mejor rendimiento en Windows (https://docs.microsoft.com/en-us/windows/wsl/)

### Comunidades:
- Docker en español: https://discord.gg/docker (canal #spanish)
- Django Hispano: https://t.me/djangohispano
- Stack Overflow en español: https://es.stackoverflow.com/

---

## 💡 Tips finales para Windows

1. **Usa WSL 2** para mejor rendimiento con Docker
2. **Coloca proyectos en WSL filesystem** cuando uses WSL 2
3. **Reinicia Docker Desktop** si algo no funciona
4. **Limpia Docker regularmente** con `docker system prune`
5. **Lee los logs** con `docker-compose logs -f` para debug
6. **Usa Postman** en lugar de curl en Windows (más fácil)
7. **No cierres Docker Desktop** mientras los contenedores corren
8. **Asigna suficiente RAM** en Docker Desktop Settings (min 4GB)

---

## 🎯 Próximos pasos sugeridos

1. **Experimenta**: Rompe cosas, arregla cosas, aprende
2. **Crea endpoints nuevos**: Practica CRUD con otros modelos
3. **Agrega validaciones**: Mejora los serializers
4. **Implementa permisos**: Usuarios solo editan su perfil
5. **Agrega tests**: Aprende TDD con Django
6. **Dockeriza otros proyectos**: Aplica lo aprendido

---

**¿Dudas?** Revisa la sección de Troubleshooting o los logs con `docker-compose logs -f`

**¡Éxito con Docker en Windows!** 🐳🪟✨