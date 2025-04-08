class AppError(Exception):
    """Excepción base para la aplicación."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return self.message

    def to_dict(self):
        return {"message": self.message, "status_code": self.status_code}


class NotFoundError(AppError):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)


class ValidationError(AppError):
    def __init__(self, message="Validation error"):
        super().__init__(message, status_code=400)


class ConflictError(AppError):
    def __init__(self, message="Conflict error"):
        super().__init__(message, status_code=409)


class UnauthorizedError(AppError):
    def __init__(self, message="Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenError(AppError):
    def __init__(self, message="Forbidden"):
        super().__init__(message, status_code=403)
