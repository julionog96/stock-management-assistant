from sqlalchemy.orm import Session
from app.models.stock import StockThreshold

'''
Serviço que gerencia os thresholds de estoque.
Será consultado antes de chamar a LLM para tomar uma decisão.
'''


class ThresholdService:

    @staticmethod
    def get_threshold(
        db: Session,
        tenant_id: int,
        product_id: int
    ) -> StockThreshold | None:
        if not tenant_id:
            raise ValueError("Tenant ID is required")
        if not product_id:
            raise ValueError("Product ID is required")
          
        stock_threshold_query = db.query(StockThreshold).filter(
            StockThreshold.tenant_id == tenant_id,
            StockThreshold.product_id == product_id
        )
        return stock_threshold_query.first()

    @staticmethod
    def update_threshold(
        db: Session,
        tenant_id: int,
        product_id: int,
        minimum_quantity: int
    ) -> StockThreshold:
        if not tenant_id:
            raise ValueError("Tenant ID is required")
        if not product_id:
            raise ValueError("Product ID is required")
        if not minimum_quantity:
            raise ValueError("Minimum quantity is required")
          
        threshold = ThresholdService.get_threshold(db, tenant_id, product_id)

        if not threshold:
            threshold = StockThreshold(
                tenant_id=tenant_id,
                product_id=product_id,
                minimum_quantity=minimum_quantity
            )
            db.add(threshold)
        else:
            threshold.minimum_quantity = minimum_quantity

        db.commit()
        db.refresh(threshold)
        return threshold
