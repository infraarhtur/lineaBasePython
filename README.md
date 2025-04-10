# lineaBasePython
Este es un proyecto en fastApi en el cual demostrare un CRUD conectandome a AWS
intento que este proyecto me sirva como estudio y guia para otros proyectos 


# arquitectura inicial
```

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

```
# requirements

# comandos docker
Docker ps -a
docker logs linea_base_app   
docker-compose down

### elimina con con volumenes 
docker-compose down --volumes 

###  ver que volumenes existen
docker volume ls

docker-compose up -d --build

### inspeccionar pgdata
docker volume inspect pgdata

--------------------------------------------------------------------------------
Puedes entrar al contenedor de la base de datos:
docker exec -it linea_base_db bash

Luego accede a PostgreSQL con:
psql -U postgres -d postgres


Y verifica las tablas existentes

\dt
