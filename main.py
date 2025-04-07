# main.py
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Config
from app.data.database import Base, engine
from app.workers.scheduler import start_worker  # Importar el worker
from app.view.client_endpoints import router as client_router
from app.view.products_endpoints import router as product_router
from app.view.category_endpoints import router as category_router

# load_dotenv()

# print(os.getenv("AWS_ACCESS_KEY_ID"))
# print(os.getenv("AWS_SECRET_ACCESS_KEY"))


# print(os.getenv("AWS_ACCESS_KEY_ID"))
# print(os.getenv("AWS_SECRET_ACCESS_KEY"))
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
    description="A FastAPI-based system for managing clients and products.",
    version=app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las solicitudes de cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Incluir el router
app.include_router(client_router, prefix="/api/clients", tags=["Clients"])
app.include_router(product_router, prefix="/api/products", tags=["Products"])
app.include_router(category_router, prefix="/api/category", tags=["Categories"])

# Iniciar el worker cuando se inicia la aplicación
@app.on_event("startup")
def startup_event():
    print("[Main] Iniciando aplicación y worker...")
    start_worker()

@app.on_event("shutdown")
def shutdown_event():
    print("[Main] Apagando aplicación y worker...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=app_host, port=app_port)
