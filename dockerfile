# Usamos una imagen oficial de Python ligera compatible con Apple Silicon
FROM python:3.13-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements/dev.txt

# Exponer el puerto (asumiendo que FastAPI corre en el 8000)
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
