from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    stocks = relationship("Stock", back_populates="tenant")

    def __repr__(self):
        return f"Tenant(id={self.id}, name={self.name})"