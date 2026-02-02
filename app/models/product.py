from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    stocks = relationship("Stock", back_populates="product")

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name})"
