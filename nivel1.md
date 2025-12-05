# 🟦 Nivel 1: Mejora del Proyecto con Docker — Dev Mode & Deploy Mode

Este documento explica detalladamente los ajustes implementados en el **Nivel 1**, los cambios aplicados al proyecto y cómo arrancar el sistema correctamente tanto en **modo desarrollo** como en **modo producción**, junto con sus diferencias clave.

---

# 📘 1. ¿Qué incluye el Nivel 1?

El Nivel 1 mejora la estructura general del proyecto agregando:

1. ✔ **Archivo `.env`** para manejar variables de entorno.  
2. ✔ **docker-compose.yml actualizado** para usar variables del `.env`.  
3. ✔ **docker-compose.override.yml** para ejecutar el proyecto en modo desarrollo.  
4. ✔ **Healthcheck para Django y PostgreSQL**.  
5. ✔ **Gunicorn como servidor de producción**.  
6. ✔ **Separación real entre Dev Mode y Deploy Mode**.

Estas mejoras te permiten trabajar de manera profesional y aprender conceptos reales de Docker.

---

# 📁 2. Archivos creados o modificados en este nivel

## ✔ `.env`  
Variables de entorno centralizadas para evitar hardcodeo.

## ✔ `docker-compose.yml`  
Archivo principal usado en producción.

## ✔ `docker-compose.override.yml`  
Archivo usado automáticamente en desarrollo.

## ✔ `settings.py`  
Actualizado para leer valores desde variables de entorno.

## ✔ `Dockerfile`  
Actualizado para incluir `curl` y `gunicorn`.

---

# 🚀 3. Cómo arrancar el proyecto en cada modo

---

# 🟢 DEV MODE (modo desarrollo)

### ✔ ¿Qué características tiene Dev Mode?
- Usa `docker-compose.yml` + `docker-compose.override.yml`
- Django corre con **runserver**
- Código del host → contenedor (hot reload)
- Depuración ON
- Ideal para programar

### 🎯 Comando para iniciar en dev:
```bash
docker-compose up --build
```

### 🎯 Comando para detener en dev:
```bash
docker-compose down
```

### 🔍 Confirmación visual:

En los logs verás:
```rust
Watching for file changes...
Starting development server at http://0.0.0.0:8000
```

---

# 🔵 DEPLOY MODE (modo producción)

### ✔ ¿Qué características tiene Deploy Mode?

- Usa solo docker-compose.yml
- No usa override
- Django corre con Gunicorn
- No existe hot reload
- DEBUG desactivado
- Volúmenes más controlados

### 🎯 Comando para iniciar en producción:
```bash
docker-compose -f docker-compose.yml up --build -d
```

### 🎯 Para ver logs:
```bash
docker-compose logs -f
```

### 🎯 Para detener:
```bash
docker-compose -f docker-compose.yml down
```

### 🔍 Confirmación visual:

En los logs verás:
```rust
[INFO] Starting gunicorn...
[INFO] Booting worker with pid...
```

---

# ⚖️ 4. Diferencias clave entre Dev Mode y Deploy Mode

| Característica | 	Dev Mode | 	Deploy Mode | 
| Servidor | 	runserver |  	Gunicorn | 
| Hot Reload |  	✔ Sí	|   ❌ No | 
| Volúmenes | 	✔ Montados	|  ❌ No montados | 
| DEBUG | 	✔ Activado	|  ❌ Desactivado | 
| Archivos |  usados	|  docker-compose.yml + override.yml	docker-compose.yml | 
| Ideal |  para	Programar	|  Producción / pruebas reales | 

---

# 📊 5. Flujo de archivos utilizados por Docker

## 🟢 Dev Mode:

```bash
docker-compose.yml
+ docker-compose.override.yml
--------------------------------
= Configuración combinada para desarrollo
```

## 🔵 Deploy Mode:

```bash
docker-compose.yml
--------------------------------
= Configuración única optimizada para producción
```

---

# 🔧 6. Comandos útiles según el modo

## 🟢 Desarrollo

```bash
docker-compose up
docker-compose up --build
docker-compose down
docker-compose exec web bash
```


## 🔵 Producción

```bash
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml restart
docker-compose -f docker-compose.yml down
docker-compose logs -f
```

---

# 🎓 7. Qué has aprendido en este nivel

✔ Diferencia entre override y compose normal
✔ Separación entre entornos desarrollo y producción
✔ Cómo usar .env en Docker
✔ Cómo levantar Gunicorn con Django
✔ Cómo aplicar healthchecks en contenedores
✔ Cómo leer variables de entorno desde Django
✔ Cómo Docker combina configuraciones