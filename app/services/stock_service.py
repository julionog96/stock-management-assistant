from sqlalchemy.orm import Session, joinedload
from app.models.stock import Stock

DEFAULT_MINIMUM_QUANTITY = 10


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
    def get_stock_with_details(
        db: Session,
        tenant_id: int,
        product_id: int
    ) -> Stock | None:
        """Retorna o estoque com tenant e product carregados."""
        if not tenant_id:
            raise ValueError("Tenant ID is required")
        if not product_id:
            raise ValueError("Product ID is required")

        return (
            db.query(Stock)
            .options(
                joinedload(Stock.tenant),
                joinedload(Stock.product),
            )
            .filter(
                Stock.tenant_id == tenant_id,
                Stock.product_id == product_id,
            )
            .first()
        )

    @staticmethod
    def update_stock(
        db: Session,
        tenant_id: int,
        product_id: int,
        quantity: int,
        minimum_quantity: int | None = None
    ) -> Stock:
        stock = StockService.get_stock(db, tenant_id, product_id)

        if not stock:
            stock = Stock(
                tenant_id=tenant_id,
                product_id=product_id,
                quantity=quantity,
                minimum_quantity=DEFAULT_MINIMUM_QUANTITY
            )
            db.add(stock)
        else:
            stock.quantity = quantity

        db.commit()
        db.refresh(stock)
        return stock

    @staticmethod
    def update_threshold(
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

        stock = StockService.get_stock(db, tenant_id, product_id)
        if not stock:
            raise ValueError("Stock not found")

        stock.minimum_quantity = minimum_quantity
        db.commit()
        db.refresh(stock)
        return stock
