class AppError(Exception):
    """Excepción base para la aplicación."""
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.status_code = status_code

class NotFoundError(AppError):
    """Excepción para recursos no encontrados."""
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)

class ValidationError(AppError):
    """Excepción para errores de validación."""
    def __init__(self, message="Validation error"):
        super().__init__(message, status_code=400)
