from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    product_id = Column(
        Integer, ForeignKey("products.id"), nullable=False
        )

    quantity = Column(Integer, nullable=False)
    minimum_quantity = Column(Integer, default=10, nullable=False)
