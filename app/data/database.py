import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import Config

# Cargar variables de entorno
load_dotenv()

# Configuración desde config.yaml
config = Config("config.yaml")
# Detectar si estamos en Docker (variable típica en contenedores)
# running_in_docker = os.environ.get("RUNNING_IN_DOCKER", "false").lower() == "true"

# Elegir la conexión correcta
# DATABASE_URL = os.environ["DB_URL_DOCKER"] if running_in_docker else os.environ["DB_URL_LOCAL"]
# Obtener la URL de la base de datos
DATABASE_URL = os.getenv("DB_URL")
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
    except  Exception as e:
        print(f'Error de session {e}')
    finally:
        db.close()
