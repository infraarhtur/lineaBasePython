import uuid
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.provider_model import ProviderModel


class ProviderRepository:
    """
    Repositorio que maneja el acceso a datos para proveedores.
    """

    def __init__(self, db: Session):
        self.db = db

    def save(self, provider: ProviderModel) -> ProviderModel:
        """
        Guarda un proveedor en la base de datos (crear o actualizar).

        Args:
            provider (ProviderModel): Proveedor a guardar.

        Returns:
            ProviderModel: Proveedor guardado.
        """
        try:
            self.db.add(provider)
            self.db.commit()
            self.db.refresh(provider)
            return provider
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def fetch(self, provider_id: uuid.UUID) -> Optional[ProviderModel]:
        """
        Recupera un proveedor por ID.

        Args:
            provider_id (uuid.UUID): ID del proveedor.

        Returns:
            Optional[ProviderModel]: Proveedor encontrado o None.
        """
        try:
            return self.db.query(ProviderModel).filter(ProviderModel.id == provider_id).first()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def fetch_all(self) -> List[ProviderModel]:
        """
        Recupera todos los proveedores de la base de datos.

        Returns:
            List[ProviderModel]: Lista de proveedores.
        """
        try:
            return self.db.query(ProviderModel).all()
        except SQLAlchemyError as e:
            raise e

    def delete(self, provider: ProviderModel) -> bool:
        """
        Elimina un proveedor de la base de datos.

        Args:
            provider (ProviderModel): Proveedor a eliminar.

        Returns:
            bool: True si se eliminó correctamente.
        """
        try:
            self.db.delete(provider)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
