import time
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Crear un scheduler asíncrono
scheduler = AsyncIOScheduler()

async def my_scheduled_task():
    """Tarea asíncrona que se ejecuta cada 30 segundos."""
    print(f"[Worker] Ejecutando tarea... {time.strftime('%Y-%m-%d %H:%M:%S')}")
    await asyncio.sleep(1)  # Simulación de tarea async (puede ser una consulta a BD, API, etc.)

def start_worker():
    """Función para iniciar el scheduler en segundo plano."""
    if not scheduler.running:
        print("[Worker] Iniciando APScheduler (Asíncrono)...")
        scheduler.add_job(my_scheduled_task, "interval", seconds=30)
        scheduler.start()
