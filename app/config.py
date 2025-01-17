# app/config.py
import yaml
from typing import Any

class Config:
    """
    Clase para manejar la configuración de la aplicación.
    Permite cargar un archivo YAML y obtener valores específicos.
    """

    def __init__(self, config_file: str):
        """
        Constructor de la clase Config.

        Args:
            config_file (str): Ruta al archivo de configuración YAML.
        """
        self.config = self._load_config(config_file)

    def _load_config(self, config_file: str) -> dict:
        """
        Carga el archivo de configuración YAML.

        Args:
            config_file (str): Ruta al archivo de configuración.

        Returns:
            dict: Contenido del archivo de configuración como un diccionario.
        """
        try:
            with open(config_file, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo de configuración '{config_file}' no se encontró.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error al procesar el archivo YAML: {e}")

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor específico de la configuración.

        Args:
            section (str): Sección de la configuración.
            key (str): Clave dentro de la sección.
            default (Any): Valor por defecto si no se encuentra la clave.

        Returns:
            Any: Valor correspondiente a la clave o el valor por defecto.
        """
        return self.config.get(section, {}).get(key, default)
