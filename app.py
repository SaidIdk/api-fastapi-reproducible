from fastapi import FastAPI

app = FastAPI(
    title="API de ejemplo",
    description="API mínima creada con FastAPI para la sesión de hoy.",
    version="1.0.0",
)


@app.get("/", tags=["Inicio"])
def read_root():
    return {"mensaje": "¡Hola! La API está funcionando."}


@app.get("/saludo/{nombre}", tags=["Saludos"])
def greet(nombre: str):
    return {"mensaje": f"Hola, {nombre}!"}


@app.get("/health", tags=["Estado"])
def health_check():
    return {"estado": "ok"}
