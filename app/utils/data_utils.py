from datetime import datetime

def format_date(date_str, input_format="%Y-%m-%d", output_format="%d/%m/%Y"):
    """Convierte una fecha de un formato a otro."""
    try:
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}")

def is_valid_email(email):
    """Valida si un email tiene un formato correcto."""
    import re
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None
