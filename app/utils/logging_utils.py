import logging

def setup_logging(level=logging.INFO, log_format=None):
    """Configura el sistema de logging."""
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=level, format=log_format)

def get_logger(name):
    """Obtiene un logger con el nombre dado."""
    return logging.getLogger(name)
