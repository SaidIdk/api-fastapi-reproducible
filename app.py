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
    inversion_publicidad: float = Field(..., example=200.0, description="Monto invertido en publicidad (S/)")
    dias_campana: int = Field(..., example=5, description="Duración de la campaña en días")


def cargar_dataset():
    fallback = [{"id": 1, "nombre": "Muestra inicial", "version": "v1.0.0"}]
    if not DATA_PATH.exists():
        return fallback
    for enc in ("utf-8-sig", "utf-16"):
        try:
            with open(DATA_PATH, "r", encoding=enc) as f:
                return json.load(f)
        except Exception:
            continue
    return fallback


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
    if isinstance(dataset, list) and len(dataset) > 0 and isinstance(dataset[0], dict):
        version = dataset[0].get("version", "v1.0.0")
    elif isinstance(dataset, dict):
        version = dataset.get("version", "v1.0.0")
    else:
        version = "v1.0.0"

    base = 120.0
    peso_inversion = 3.2
    peso_dias = 15.5

    aporte_inversion = round(datos.inversion_publicidad * peso_inversion, 2)
    aporte_dias = round(datos.dias_campana * peso_dias, 2)
    ventas_estimadas = round(base + aporte_inversion + aporte_dias, 2)

    return {
        "entrada": {
            "inversion_publicidad": datos.inversion_publicidad,
            "dias_campana": datos.dias_campana,
        },
        "proceso_calculo": {
            "ecuacion": "ventas = 120.0 + (inversion * 3.2) + (dias * 15.5)",
            "paso_1_base": base,
            "paso_2_inversion": f"{datos.inversion_publicidad} * {peso_inversion} = {aporte_inversion}",
            "paso_3_dias": f"{datos.dias_campana} * {peso_dias} = {aporte_dias}",
            "paso_4_total": f"{base} + {aporte_inversion} + {aporte_dias} = {ventas_estimadas}",
        },
        "ventas_estimadas": ventas_estimadas,
        "rendimiento": "Alto" if ventas_estimadas >= 1500 else "Moderado",
        "modelo": "Regresión Lineal v1.0.0",
        "dataset_version": version,
    }
