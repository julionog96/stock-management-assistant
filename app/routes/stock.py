from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.stock_service import StockService

router = APIRouter(prefix="/stocks")


@router.get("/{tenant_id}/{product_id}")
def get_stock(
    tenant_id: int,
    product_id: int,
    db: Session = Depends(get_db)
):
    stock = StockService.get_stock(
        db=db,
        tenant_id=tenant_id,
        product_id=product_id
    )

    if not stock:
        return {"quantity": 0}

    return {
        "tenant_id": tenant_id,
        "product_id": product_id,
        "quantity": stock.quantity
    }
