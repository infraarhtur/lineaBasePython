# app/data/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from app.config import Config
# Cargar variables de entorno
load_dotenv()
#configuracion llaves
config = Config("config.yaml")

# Configuración de la base de datos
DATABASE_URL = config.get("database","url")

# Crear el motor de la base de datos
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

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





# # app/data/database.py
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# # Configuración de la base de datos
# DATABASE_URL = "sqlite:////Users/arthur/Bases de datos/lineaBase"

# # Crear el motor de la base de datos
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# # Crear la sesión
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base para modelos
# Base = declarative_base()

# # Dependencia para obtener la sesión de la base de datos
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
