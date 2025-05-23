from typing import Optional
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.data.sale_repository import SaleRepository
from app.models.sale_details_model import SaleDetailModel

# from app.models.sale_schema import SaleCreateSchema
from app.models.sale_model import SaleCreateSchema, SaleModel, SaleUpdateSchema


class SaleLogic:
    def __init__(self, db: Session):
        self.db = db
        self.sale_repo = SaleRepository(db)



    def get_all_sales(self):
        return self.sale_repo.get_all()

    def get_sale_by_id(self, sale_id: UUID):
        return self.sale_repo.get_by_id(sale_id)

    def delete_sale(self, sale_id: UUID) -> bool:
        sale = self.sale_repo.get_by_id(sale_id)
        if not sale:
            return False
        return self.sale_repo.delete(sale)
    
    def create_sale(self, sale_data: SaleCreateSchema) -> SaleModel:
        try:
            # Crear la venta principal
            sale = SaleModel(
                client_id=sale_data.client_id,
                sale_date=sale_data.sale_date,
                total_amount=sale_data.total_amount,
                status=sale_data.status,
                payment_method=sale_data.payment_method,
                comment=sale_data.comment,
                created_by=sale_data.created_by
            )

            # Crear los detalles de la venta
            for detail in sale_data.details:
                sale_detail = SaleDetailModel(
                    product_id=detail.product_id,
                    quantity=detail.quantity,
                    discount=detail.discount,
                    tax=detail.tax,
                    subtotal=detail.subtotal,
                    total=detail.total,
                    unit_cost=detail.unit_cost,
                    comment=detail.comment
                )
                sale.details.append(sale_detail)

            response = self.sale_repo.save(sale)
            return response

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
        
    def update_sale(self, sale_id: UUID, update_data: SaleUpdateSchema) -> Optional[SaleModel]:

        sale = self.get_sale_by_id(sale_id)
         #self.db.query(SaleModel).filter(SaleModel.id == sale_id).first()

        if not sale:
            return None

        if update_data.client_id is not None:
            sale.client_id = update_data.client_id
        if update_data.sale_date is not None:
            sale.sale_date = update_data.sale_date
        if update_data.total_amount is not None:
            sale.total_amount = update_data.total_amount
        if update_data.status is not None:
            sale.status = update_data.status
        if update_data.payment_method is not None:
            sale.payment_method = update_data.payment_method
        if update_data.comment is not None:
            sale.comment = update_data.comment
        if update_data.created_by is not None:
            sale.created_by = update_data.created_by

        try:
            # self.db.commit()
            # self.db.refresh(sale)
            response = self.sale_repo.save(sale)
            return response
        except:
            self.db.rollback()
            raise