import json
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="API de Predicción de Ventas",
    description="API reproducible con modelo de regresión lineal, versionado de datos y Swagger UI.",
    version="1.0.0",
)

DATA_PATH = Path("data/v1/dataset.json")


class DatosCampana(BaseModel):
    inversion_publicidad: float = Field(..., example=500.0, description="Monto invertido en publicidad (S/)")
    dias_campana: int = Field(..., example=15, description="Duración de la campaña en días")


def cargar_dataset():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return [{"id": 1, "nombre": "Muestra inicial", "version": "v1.0.0"}]


@app.get("/", tags=["Inicio"])
def read_root():
    return {"mensaje": "¡Hola! La API de predicción está funcionando."}


@app.get("/saludo/{nombre}", tags=["Saludos"])
def greet(nombre: str):
    return {"mensaje": f"Hola, {nombre}!"}


@app.get("/health", tags=["Estado"])
def health_check():
    return {"estado": "ok"}


@app.get("/datos", tags=["Datos"])
def obtener_datos():
    return {"version_dataset": "v1.0.0", "registros": cargar_dataset()}


@app.post("/predecir", tags=["Predicción"])
def predecir_ventas(datos: DatosCampana):
    dataset = cargar_dataset()
    version = dataset[0].get("version", "v1.0.0") if dataset else "v1.0.0"
    ventas_estimadas = round(120.0 + (datos.inversion_publicidad * 3.2) + (datos.dias_campana * 15.5), 2)
    return {
        "inversion_publicidad": datos.inversion_publicidad,
        "dias_campana": datos.dias_campana,
        "ventas_estimadas": ventas_estimadas,
        "rendimiento": "Alto" if ventas_estimadas >= 1500 else "Moderado",
        "modelo": "Regresión Lineal v1.0.0",
        "dataset_version": version,
    }
