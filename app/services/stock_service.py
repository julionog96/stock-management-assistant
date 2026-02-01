from sqlalchemy.orm import Session
from app.models.stock import Stock


class StockService:
    '''
    Classe de serviços para gerenciar o estoque
    '''

    @staticmethod
    def get_stock(
        db: Session,
        tenant_id: int,
        product_id: int
    ) -> Stock | None:
        if not tenant_id:
            raise ValueError("Tenant ID is required")
        if not product_id:
            raise ValueError("Product ID is required")
          
        stock_query = db.query(Stock).filter(
            Stock.tenant_id == tenant_id,
            Stock.product_id == product_id
        )
        return stock_query.first()

    @staticmethod
    def update_stock(
        db: Session,
        tenant_id: int,
        product_id: int,
        quantity: int
    ) -> Stock:
        stock = StockService.get_stock(db, tenant_id, product_id)

        if not stock:
            stock = Stock(
                tenant_id=tenant_id,
                product_id=product_id,
                quantity=quantity
            )
            db.add(stock)
        else:
            stock.quantity = quantity

        db.commit()
        db.refresh(stock)
        return stock
