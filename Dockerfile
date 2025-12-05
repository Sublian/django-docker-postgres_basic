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
    curl \
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