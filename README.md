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

La API estará disponible en:

```
http://localhost:8000/api/
```

### Detener contenedores

```bash
docker-compose down
```

### 🔹 Modo Producción (simulado)

``` bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

------------------------------------------------------------------------

## 📡 Endpoints Principales

### Auth

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | /api/login/ | Login con JWT |
| POST | /api/refresh/ | Refresh token |
| GET | /api/protected/ | Vista protegida |



### Productos

| Método | Endpoint | Descripción |
| GET | /api/products/ | Listar productos |
| POST | /api/products/ | Crear producto (staff/admin) |
| DELETE | /api/products/{id}/ | Eliminar (solo admin) |

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

## 🧑‍💻 Usuarios de Prueba

Se generan automáticamente:

- Clientes
- Staff
- Admin

Y productos falsos usando Faker.

---

## 🗄️ Acceso a la Base de Datos (PostgreSQL en Docker)

⚠️ Este proyecto **NO usa el usuario `postgres` por defecto**. Se define un usuario personalizado en el archivo `.env`:

```env
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_pass
POSTGRES_DB=django_db
```

### ✅ Comando correcto para acceder a la BD

```bash
docker-compose exec db psql -U django_user -d django_db
```

### ❌ Comando incorrecto (generará error)

```bash
docker-compose exec db psql -U postgres
```

### 📌 Comandos útiles dentro de PostgreSQL

```sql
\l      -- listar bases de datos
\dt     -- listar tablas
\du     -- listar usuarios
```

Ejemplos:

```sql
SELECT * FROM users_customuser;
SELECT * FROM products_product;
```

---

## 🛡️ Seguridad Implementada

- JWT con rotación
- Blacklist de refresh tokens
- Rate limiting en login
- Validaciones por rol



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

---

## 🎯 Objetivo del Repositorio

Este proyecto funciona como **plantilla base reutilizable** para futuros proyectos:

- APIs seguras
- Backend moderno
- Tests incluidos desde el inicio
- Docker listo para producción

------------------------------------------------------------------------

# 🚀 100% Test Coverage Achieved

**Professional Django REST API with Full Test Coverage • Docker • JWT • PostgreSQL**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django 4.2](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![Coverage 100%](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)](#)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🏆 The Achievement: 100% Test Coverage

**After an intensive testing sprint, this project has achieved 100% test coverage** - a rare accomplishment in real-world Django projects. Every line of code is verified by comprehensive automated tests.

### 📊 Coverage Statistics
- **Total Coverage:** 100% ✅
- **Test Files:** 10+
- **Total Tests:** 62 passing tests
- **Lines of Code:** 265 (all covered)

### 🧪 Testing Excellence
- **100% test coverage** across all modules
- **Pytest** with advanced fixtures and parametrization
- **Factory Boy** for clean test data
- **Mocking** external dependencies
- **Integration tests** for all API endpoints

---

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

Proyecto educativo para aprendizaje y reutilización.
