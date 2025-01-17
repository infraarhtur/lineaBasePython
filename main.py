# main.py
from fastapi import FastAPI
from app.view.client_endpoints import router
from app.data.database import Base, engine
from app.config import Config

import os

# Crear el directorio para la base de datos si no existe
os.makedirs("data", exist_ok=True)

# Inicializar la base de datos
Base.metadata.create_all(bind=engine)

# Cargar configuración
config = Config("config.yaml")
app_name = config.get("app", "name", default="Client Management System")
app_version = config.get("app", "version", default="1.0.0")
app_host = config.get("app", "host", default="127.0.0.1")
app_port = config.get("app", "port", default=8000)

# Crear la aplicación FastAPI
app = FastAPI(
    title=app_name,
    description="A FastAPI-based system for managing clients.",
    version=app_version,
)

# Incluir el router
app.include_router(router, prefix="/api", tags=["Clients"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=app_host, port=app_port)
