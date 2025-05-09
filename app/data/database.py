import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import Config

# Cargar variables de entorno
load_dotenv()

# Configuración desde config.yaml
config = Config("config.yaml")

if os.getenv("DB_URL") is not None:
    DATABASE_URL = os.getenv("DB_URL")
else:
     DATABASE_URL = os.getenv("DB_URL_LOCAL")

SCHEMA = os.getenv("SCHEMA", "public")

print(f"✅ Conectando a la base de datos en: {DATABASE_URL}")  # DEBUG

SCHEMA = config.get("database", "schema") or "public"

# Crear el motor de la base de datos con soporte para esquemas
engine = create_engine(f"{DATABASE_URL}?options=-csearch_path%3D{SCHEMA}")

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    """
    Proporciona una sesión de base de datos para interactuar con la base de datos.

    Yields:
        Session: Una sesión activa de SQLAlchemy.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
