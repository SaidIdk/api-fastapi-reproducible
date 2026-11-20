import json
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="API de ejemplo con Predicción",
    description="API funcional y reproducible creada con FastAPI, versionado de datos y Swagger UI.",
    version="1.0.0",
)

DATA_PATH = Path("data/v1/dataset.json")


class DatosEntrada(BaseModel):
    valor: float


def cargar_dataset():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return [{"id": 1, "nombre": "Muestra inicial", "version": "v1.0.0"}]


@app.get("/", tags=["Inicio"])
def read_root():
    return {"mensaje": "¡Hola! La API está funcionando."}


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
def predecir(entrada: DatosEntrada):
    dataset = cargar_dataset()
    version = dataset[0].get("version", "v1.0.0") if dataset else "v1.0.0"
    prediccion = round(entrada.valor * 2.5 + 1.0, 4)
    return {
        "entrada": entrada.valor,
        "prediccion": prediccion,
        "categoria": "Alto" if prediccion >= 10 else "Normal",
        "modelo_version": "1.0.0",
        "dataset_version": version,
    }
