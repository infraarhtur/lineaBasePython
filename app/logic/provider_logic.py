import uuid
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.data.provider_repository import ProviderRepository
from app.models.provider_model import ProviderModel
from app.utils import constans as const
from app.utils.error_handling import ValidationError, NotFoundError


class ProviderLogic:
    """
    Lógica de negocio para los proveedores.
    """

    def __init__(self, db: Session):
        self.db = db
        self.provider_repo = ProviderRepository(db)

    def create_provider(self, **kwargs) -> ProviderModel:
        """
        Crea un nuevo proveedor.

        Args:
            **kwargs: Datos del proveedor.

        Returns:
            ProviderModel: Proveedor creado.
        """
        try:
            if not kwargs.get("name"):
                raise ValidationError("El nombre del proveedor es obligatorio")

            provider = ProviderModel(**kwargs)
            return self.provider_repo.save(provider)

        except SQLAlchemyError as e:
            raise e

    def get_provider_by_id(self, provider_id: str) -> ProviderModel:
        """
        Recupera un proveedor por su ID.

        Args:
            provider_id (str): UUID del proveedor.

        Returns:
            ProviderModel: Proveedor encontrado.
        """
        try:
            provider_uuid = uuid.UUID(provider_id)
        except ValueError:
            raise ValidationError(const.ERROR_INVALID_UUID)

        provider = self.provider_repo.fetch(provider_uuid)

        if not provider:
            raise NotFoundError(f"Proveedor con ID '{provider_id}' no encontrado.")

        return provider

    def get_all_providers(self) -> List[ProviderModel]:
        """
        Recupera todos los proveedores.

        Returns:
            List[ProviderModel]: Lista de proveedores.
        """
        try:
            return self.provider_repo.fetch_all()
        except SQLAlchemyError as e:
            raise e

    def update_provider(self, provider_id: str, **kwargs) -> ProviderModel:
        """
        Actualiza los datos de un proveedor.

        Args:
            provider_id (str): ID del proveedor.
            **kwargs: Campos a actualizar.

        Returns:
            ProviderModel: Proveedor actualizado.
        """
        provider = self.get_provider_by_id(provider_id)

        for field, value in kwargs.items():
            if hasattr(provider, field) and value is not None:
                setattr(provider, field, value)

        return self.provider_repo.save(provider)

    def delete_provider(self, provider_id: str) -> bool:
        """
        Elimina un proveedor por su ID.

        Args:
            provider_id (str): ID del proveedor a eliminar.

        Returns:
            bool: True si fue eliminado correctamente.
        """
        provider = self.get_provider_by_id(provider_id)
        return self.provider_repo.delete(provider)
