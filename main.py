# main.py
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Config
from app.data.database import Base, engine

# Importar routers
from app.view.category_endpoints import router as category_router
from app.view.client_endpoints import router as client_router
from app.view.products_endpoints import router as product_router
from app.view.provider_endpoints import router as provider_router
from app.view.sale_endpoints import router as sale_router
from app.workers.scheduler import start_worker

# Cargar variables de entorno
load_dotenv()

# Inicializar directorio y base de datos
os.makedirs("data", exist_ok=True)
Base.metadata.create_all(bind=engine)

# Cargar configuración desde archivo
config = Config("config.yaml")
APP_NAME = config.get("app", "name", default="Client Management System")
APP_VERSION = config.get("app", "version", default="1.0.0")
APP_HOST = config.get("app", "host", default="127.0.0.1")
APP_PORT = config.get("app", "port", default=8000)

# Inicializar la aplicación FastAPI
app = FastAPI(
    title=APP_NAME,
    description="A FastAPI-based system for managing clients, products, providers and categories.",
    version=APP_VERSION,
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes limitar esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(client_router, prefix="/api/clients", tags=["Clients"])
app.include_router(product_router, prefix="/api/products", tags=["Products"])
app.include_router(category_router, prefix="/api/category", tags=["Categories"])
app.include_router(provider_router, prefix="/api/provider", tags=["Providers"])
app.include_router(sale_router, prefix="/api/sale", tags=["Sales"])

# Eventos de arranque y apagado
@app.on_event("startup")
def on_startup():
    print("[Main] Iniciando aplicación y worker...")
    start_worker()

@app.on_event("shutdown")
def on_shutdown():
    print("[Main] Apagando aplicación y worker...")

# Ejecución con Uvicorn si es llamado directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT, reload=True)
    #
