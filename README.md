# API mínima con FastAPI

Proyecto desplegado y configurado bajo estándares de reproducibilidad (entorno fijado con `requirements.txt`, contenedorización con `Dockerfile` y versionado de datos).

## Enlace desplegado

- **API en producción:** `api-fastapi-reproducible.onrender.com`
- **Documentación interactiva (Swagger UI):** `api-fastapi-reproducible.onrender.com/docs`

## 1. Reproducibilidad del entorno

Requiere Python 3.10 o posterior (congelado en Python 3.14.7). Las versiones exactas de las dependencias están fijadas en `requirements.txt`.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install --no-cache-dir -r requirements.txt
fastapi dev app.py
