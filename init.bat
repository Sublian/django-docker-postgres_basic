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