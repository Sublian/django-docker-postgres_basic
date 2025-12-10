# 🚀 Django API Template --- Docker • JWT • Roles • Tests

**Modern Dev Template for Real Projects**

![Status](https://img.shields.io/badge/status-template-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![PostgreSQL](https://img.shields.io/badge/Postgres-15-lightblue)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Tests](https://img.shields.io/badge/Tests-Pytest-success)
![License](https://img.shields.io/badge/license-MIT-yellow)

------------------------------------------------------------------------

## 📦 Sobre el Proyecto

Este repositorio es una **plantilla profesional reutilizable** basada
en:

-   ✅ Autenticación JWT con Refresh Token
-   ✅ Rotación y blacklist de tokens
-   ✅ Sistema de roles (admin, staff, client)
-   ✅ Módulo de productos desacoplable
-   ✅ Rate limiting contra fuerza bruta
-   ✅ Tests automatizados con Pytest
-   ✅ 100% Dockerizado

Pensado como **base para futuros SaaS, APIs privadas, backends móviles y
microservicios**.

------------------------------------------------------------------------

## ⚙️ Stack Tecnológico

-   Django 4.2
-   Python 3.11
-   Django REST Framework
-   PostgreSQL 15
-   SimpleJWT (con rotación)
-   Pytest + Factory Boy + Faker
-   Docker & Docker Compose

------------------------------------------------------------------------

## 🧱 Arquitectura General

Client → API (Django) → Auth (JWT + Roles) → PostgreSQL

------------------------------------------------------------------------

## 🔐 Seguridad Implementada

-   JWT Access + Refresh
-   Rotación automática de Refresh Tokens
-   Blacklist de tokens antiguos
-   Protección de rutas por rol
-   Rate Limiting en login

------------------------------------------------------------------------

## 🐳 Docker --- Modos de Ejecución

### 🔹 Modo Desarrollo

``` bash
docker-compose up --build
```

### 🔹 Modo Producción (simulado)

``` bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

------------------------------------------------------------------------

## 📡 Endpoints Principales

### Auth

  Método   Endpoint              Descripción
  -------- --------------------- --------------------
  POST     /api/login/           Login JWT
  POST     /api/token/refresh/   Refresh token
  POST     /api/logout/          Logout + Blacklist
  GET      /api/protected/       Ruta protegida

### Productos

  Método   Endpoint
  -------- ------------------------------
  GET      /api/products/
  POST     /api/products/
  DELETE   /api/products/`<id>`{=html}/

------------------------------------------------------------------------

## 🧪 Tests Automatizados

Incluye tests completos de:

-   Autenticación
-   JWT
-   Rate limiting
-   Permisos por rol
-   Productos
-   Accesos restringidos

Ejecución:

``` bash
docker-compose exec web pytest
```

------------------------------------------------------------------------

## 🧰 Precarga de Datos

Incluye comandos para generar:

-   ✅ 5 usuarios falsos
-   ✅ 20 productos de prueba

Usando Faker.

------------------------------------------------------------------------

## 🗂 Estructura del Proyecto

    project/
    ├── myproject/
    ├── users/        # CustomUser + Roles
    ├── products/     # Módulo desacoplable
    ├── tests/
    ├── docker-compose.yml
    ├── requirements.txt

------------------------------------------------------------------------

## 🗺 Roadmap Técnico

-   ✅ JWT + Refresh Rotation
-   ✅ Rate Limiting
-   ✅ Roles
-   ✅ Tests
-   🔜 Logs estructurados
-   🔜 Monitoreo
-   🔜 CI/CD

------------------------------------------------------------------------

## ✅ Conclusión

Este proyecto ya es una **plantilla backend profesional de nivel
intermedio-avanzado**, ideal para:

-   Startups
-   Proyectos personales
-   Freelance
-   Portafolio técnico
-   Formación avanzada

------------------------------------------------------------------------

## 📄 Licencia

MIT --- Uso libre para cualquier proyecto.
