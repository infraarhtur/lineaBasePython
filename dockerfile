# Usamos una imagen oficial de Python ligera compatible con Apple Silicon
FROM python:3.13-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

# Establecer usuario no root
RUN useradd -m appuser

# Definir el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios para instalar dependencias primero
COPY requirements/base.txt requirements/base.txt
COPY requirements/dev.txt requirements/dev.txt

# Copiar los archivos del proyecto al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements/dev.txt

# Cambiar el propietario de los archivos al usuario no root
RUN chown -R appuser:appuser /app

# Cambiar al usuario no root
USER appuser

# Exponer el puerto (asumiendo que FastAPI corre en el 8000)
EXPOSE 8001

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
