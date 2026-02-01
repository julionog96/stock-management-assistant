from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column[int](Integer, primary_key=True)
    tenant_id = Column[int](Integer, ForeignKey("tenants.id"), nullable=False)
    product_id = Column[int](
        Integer, ForeignKey("products.id"), nullable=False
        )

    quantity = Column[int](Integer, nullable=False)


class StockThreshold(Base):
    __tablename__ = "stock_thresholds"

    id = Column[int](Integer, primary_key=True)
    tenant_id = Column[int](Integer, ForeignKey("tenants.id"), nullable=False)
    product_id = Column[int](
        Integer, ForeignKey("products.id"), nullable=False
        )

    minimum_quantity = Column[int](Integer, nullable=False)
