# Django REST API Template

**Production-Ready • Docker • JWT • PostgreSQL • 100% Test Coverage**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django 4.2](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-lightblue)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT-orange)](https://jwt.io/)
[![Tests](https://img.shields.io/badge/Tests-Pytest-success)](https://pytest.org/)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)](https://github.com/Sublian/django-docker-postgres_basic)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A professional, reusable Django REST API template designed for real-world projects. Features complete authentication, role-based permissions, comprehensive testing, CI/CD pipeline, and full Docker containerization for both development and production environments.

---

## 📑 Table of Contents

- [What Makes This Template Special](#-what-makes-this-template-special)
- [Quick Start](#-quick-start)
  - [Development Mode](#development-mode)
  - [Production Mode](#production-mode)
- [Testing Excellence](#-testing-excellence)
- [Architecture Overview](#%EF%B8%8F-architecture-overview)
- [Security Features](#-security-features)
- [API Endpoints](#-api-endpoints)
- [Testing the API](#-testing-the-api)
- [Database Access](#%EF%B8%8F-database-access)
- [Development Tools](#%EF%B8%8F-development-tools)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Project Structure](#-project-structure)
- [Use Cases](#-use-cases)
- [Roadmap](#%EF%B8%8F-roadmap)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 What Makes This Template Special

**🏆 100% Test Coverage Achieved** — Every line of code is verified by 62+ comprehensive tests

This isn't just another Django starter. It's a battle-tested foundation built with production standards:

- ✅ **JWT Authentication** with refresh token rotation and blacklist
- ✅ **Role-Based Access Control** (Admin, Staff, Client)
- ✅ **Complete Test Suite** with Pytest, Factory Boy, and mocking
- ✅ **CI/CD Pipeline** with GitHub Actions for automated testing
- ✅ **Rate Limiting** to prevent brute force attacks
- ✅ **Fully Dockerized** with separate development and production configurations
- ✅ **PostgreSQL 15** with optimized settings
- ✅ **Modern Architecture** ready for SaaS, mobile backends, or microservices

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Development Mode

```bash
# Clone the repository
git clone https://github.com/Sublian/django-docker-postgres_basic.git
cd django-docker-postgres_basic

# Start the containers
docker-compose up --build

# Access the API
http://localhost:8000/api/
```

The development environment includes:
- Hot reload for code changes
- Debug mode enabled
- SQLite for faster iterations (optional)
- Detailed error pages

### Production Mode

```bash
# Start with production configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

The production environment includes:
- Nginx as reverse proxy
- Gunicorn as WSGI server
- PostgreSQL with optimized settings
- Static files served efficiently
- Security headers enabled

---

## 🧪 Testing Excellence

This project achieves **100% test coverage** with a comprehensive test suite covering:

- **Authentication flows** (login, token refresh, logout)
- **JWT token lifecycle** (creation, validation, rotation, blacklist)
- **Role-based permissions** (admin, staff, client access levels)
- **Rate limiting** and security features
- **API endpoints** (products CRUD, user management)
- **Edge cases** and error handling

### Run Tests

```bash
# Run all tests with coverage report
docker-compose exec web pytest

# Run with detailed coverage
docker-compose exec web pytest --cov=. --cov-report=html

# Run specific test file
docker-compose exec web pytest tests/test_auth.py

# Run with verbose output
docker-compose exec web pytest -v
```

**Coverage Statistics:**
- **Total Coverage:** 100% ✅
- **Test Files:** 10+
- **Passing Tests:** 62+
- **Lines Covered:** 265/265

---

## 🏗️ Architecture Overview

```
Client (Postman/cURL/Thunder Client)
  ↓
Nginx (Production) / Django Dev Server
  ↓
Django REST API
  ↓
JWT Auth Layer → Role Verification
  ↓
PostgreSQL 15
```

**Tech Stack:**
- **Backend:** Django 4.2, Python 3.11
- **API Framework:** Django REST Framework
- **Authentication:** SimpleJWT (with rotation)
- **Database:** PostgreSQL 15
- **Testing:** Pytest, Factory Boy, Faker
- **Containerization:** Docker & Docker Compose
- **Web Server (Production):** Nginx + Gunicorn
- **CI/CD:** GitHub Actions

---

## 🔐 Security Features

- **JWT Access + Refresh Tokens** with automatic rotation
- **Token Blacklist** for revoked refresh tokens
- **Role-Based Permissions** (admin/staff/client)
- **Rate Limiting** on authentication endpoints
- **Password Hashing** with Django's PBKDF2
- **Environment Variable Security** (credentials never hardcoded)
- **CORS Configuration** for controlled cross-origin access

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/login/` | User login, returns JWT tokens | No |
| `POST` | `/api/refresh/` | Refresh access token | No |
| `GET` | `/api/protected/` | Test protected endpoint | Yes |

### Products

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| `GET` | `/api/products/` | List all products | Authenticated |
| `POST` | `/api/products/` | Create new product | Staff/Admin |
| `GET` | `/api/products/{id}/` | Retrieve product details | Authenticated |
| `PUT/PATCH` | `/api/products/{id}/` | Update product | Staff/Admin |
| `DELETE` | `/api/products/{id}/` | Delete product | Admin only |

---

## 🧪 Testing the API

You can test the API using various HTTP clients:

### Recommended Tools

- **[Postman](https://www.postman.com/)** — Full-featured API platform
- **[Thunder Client](https://www.thunderclient.com/)** — Lightweight VS Code extension
- **[Insomnia](https://insomnia.rest/)** — Modern REST client
- **[HTTPie](https://httpie.io/)** — User-friendly command-line tool
- **cURL** — Built-in command-line tool

### Example: Login with cURL

```bash
# Login and get tokens
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Response
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# Use access token for protected endpoints
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Example: Postman Collection

A Postman collection is available in the repository for easy testing:
1. Import the collection from `/postman/Django_API_Template.json`
2. Set environment variables (base_url, access_token)
3. Start testing!

---

## 🗄️ Database Access

This project uses custom PostgreSQL credentials defined in `.env`:

```bash
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_pass
POSTGRES_DB=django_db
```

### Access PostgreSQL Container

```bash
# Connect to database
docker-compose exec db psql -U django_user -d django_db

# Useful commands inside psql
\l      # List databases
\dt     # List tables
\du     # List users
\q      # Quit

# Query examples
SELECT * FROM users_customuser;
SELECT * FROM products_product;
```

⚠️ **Note:** This project doesn't use the default `postgres` user for security best practices.

---

## 🛠️ Development Tools

### Generate Test Data

The project includes management commands to populate the database with fake data:

```bash
# Create 5 test users (clients, staff, admin)
docker-compose exec web python manage.py create_fake_users

# Create 20 sample products
docker-compose exec web python manage.py create_fake_products
```

Uses **Faker** library for realistic test data generation.

### Common Docker Commands

```bash
# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f web

# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild after changes
docker-compose up --build

# Access Django shell
docker-compose exec web python manage.py shell

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files (production)
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 🔄 CI/CD Pipeline

This project includes a **fully configured GitHub Actions workflow** for continuous integration and deployment.

### What's Automated

- ✅ **Automated Testing** on every push and pull request
- ✅ **Code Coverage Reports** generated automatically
- ✅ **Linting and Code Quality** checks
- ✅ **Docker Image Building** and validation
- ✅ **Multi-environment Testing** (Python 3.11, Django 4.2)

### Workflow Configuration

The CI/CD pipeline runs on:
- Every push to `main` branch
- Every pull request
- Manual workflow dispatch

### View Pipeline Status

Check the **Actions** tab in the GitHub repository to see:
- Build status
- Test results
- Coverage reports
- Deployment logs

### Local CI Simulation

You can run the same checks locally before pushing:

```bash
# Run tests
docker-compose exec web pytest --cov

# Check code style
docker-compose exec web flake8 .

# Run security checks
docker-compose exec web bandit -r .
```

---

## 📁 Project Structure

```
django-docker-postgres_basic/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
│       └── django.yml      # Automated testing pipeline
├── myproject/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                  # Custom user model with roles
│   ├── models.py
│   ├── views.py
│   └── serializers.py
├── products/               # Decoupled products module
│   ├── models.py
│   ├── views.py
│   └── serializers.py
├── tests/                  # Comprehensive test suite
│   ├── test_auth.py
│   ├── test_permissions.py
│   └── ...
├── nginx/                  # Nginx configuration (production)
│   └── nginx.conf
├── docker-compose.yml      # Development setup
├── docker-compose.prod.yml # Production configuration
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
├── pytest.ini              # Pytest configuration
├── .env                    # Environment variables
└── README.md
```

---

## 🎯 Use Cases

This template is perfect for:

- **SaaS Applications** requiring secure authentication
- **Mobile App Backends** with REST API needs
- **Microservices** as a foundation service
- **MVP Development** with production-ready architecture
- **Learning Projects** demonstrating best practices
- **Portfolio Projects** showcasing professional standards
- **Enterprise APIs** with role-based access control

---

## 🗺️ Roadmap

- ✅ JWT Authentication with refresh token rotation
- ✅ Role-based access control system
- ✅ Comprehensive test suite (100% coverage)
- ✅ Rate limiting for security
- ✅ Docker containerization (dev + production)
- ✅ CI/CD pipeline with GitHub Actions
- 🔜 API documentation with Swagger/ReDoc
- 🔜 Structured logging with ELK stack
- 🔜 Monitoring and health checks
- 🔜 Celery for background tasks
- 🔜 Redis caching layer
- 🔜 WebSocket support

---

## 📚 Documentation

Additional guides available in the repository:

- **[Setup Guide](setup_guide.md)** — Detailed installation and configuration
- **[Level 0 Guide](nivel0.md)** — Basic concepts and getting started
- **[Level 1 Guide](nivel1.md)** — Advanced features and customization

---

## 🤝 Contributing

This is a template project, but feedback and suggestions are welcome! Feel free to:

- Report issues
- Suggest improvements
- Fork and customize for your needs
- Share how you're using it

---

## 📄 License

This project is available for educational and commercial use. Feel free to use it as a foundation for your applications.

---

## 🙏 Acknowledgments

Built with modern Django best practices and inspired by production-grade application requirements. Special focus on testing, security, developer experience, and automated deployment.

---

**Ready to build something amazing?** Fork this template and start coding! 🚀

For questions or collaboration: **subliandev@gmail.com**
