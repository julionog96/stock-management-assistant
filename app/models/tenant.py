from sqlalchemy import Column, Integer, String
from app.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column[int](Integer, primary_key=True)
    name = Column[str](String, nullable=False)
