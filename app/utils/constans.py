# app/utils/constants.py

# Error messages
ERROR_INVALID_UUID = "The provided ID is not a valid UUID."
ERROR_CLIENT_NOT_FOUND = "Client with ID '{client_id}' not found."
ERROR_EMAIL_ALREADY_EXISTS = "A client with the email '{email}' already exists."
ERROR_MISSING_REQUIRED_FIELDS = "Name and email are required fields."
ERROR_NOT_FOUND = "The requested resource was not found."
ERROR_VALIDATION = "The provided data is not valid."
ERROR_INTERNAL_SERVER = "An internal server error occurred. Please try again later."
ERROR_PRODUCT_NOT_FOUND = "product with ID '{product_id}' not found."


# Códigos de estado HTTP
HTTP_STATUS_OK = 200
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500

# Configuraciones
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Formatos comunes
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Otros
APP_NAME = "Client Management System"
APP_VERSION = "1.0.0"
