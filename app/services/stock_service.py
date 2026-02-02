from sqlalchemy.orm import Session
from app.models.stock import Stock


class StockService:
    '''
    Classe de serviços para gerenciar o estoque
    '''

    def get_stock(
        self,
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

    def update_threshold(
        self,
        db: Session,
        tenant_id: int,
        product_id: int,
        minimum_quantity: int
    ) -> Stock:
        if not tenant_id:
            raise ValueError("Tenant ID is required")
        if not product_id:
            raise ValueError("Product ID is required")
        if not minimum_quantity:
            raise ValueError("Minimum quantity is required")
         
        stock = self.get_stock(db, tenant_id, product_id)
        if not stock:
            raise ValueError("Stock not found")

        stock.minimum_quantity = minimum_quantity
        db.commit()
        db.refresh(stock)
        return stock
