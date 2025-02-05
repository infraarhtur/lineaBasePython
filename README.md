# lineaBasePython
Este es un proyecto en fastApi en el cual demostrare un CRUD conectandome a AWS
intento que este proyecto me sirva como estudio y guia para otros proyectos 


# arquitectura inicial

Copia de lineaBasePython/
│── .gitignore
│── .env
│── .python-version
│── config.yaml
│── README.md
│── main.py                    # Punto de entrada de la aplicación FastAPI
│
├── app/
│   ├── __init__.py
│   ├── config.py               # Configuración de la aplicación
│   ├── database/               # Capa de base de datos
│   │   ├── __init__.py
│   │   ├── connection.py       # Configuración de la conexión a la BD
│   │   ├── models.py           # Definición de modelos (SQLAlchemy/Pydantic)
│   │   ├── migrations/         # Scripts de migración si se usa ORM
│   ├── logic/                  # Capa de lógica de negocio
│   │   ├── __init__.py
│   │   ├── client_logic.py     # Lógica de negocio para clientes
│   ├── services/               # Capa de servicios
│   │   ├── __init__.py
│   │   ├── client_service.py   # Servicios relacionados con clientes
│   ├── view/                   # Capa de exposición de Endpoints (FastAPI)
│   │   ├── __init__.py
│   │   ├── client_endpoints.py # Definición de rutas de la API
│   ├── utils/                   # Capa de utilidades
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── error_handling.py    # Manejo de errores centralizado
│   │   ├── data_utils.py        # Funciones auxiliares para manipulación de datos


# requirements

