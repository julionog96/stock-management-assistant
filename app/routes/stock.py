from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.stock_service import StockService
from app.auth.auth import get_current_tenant

router = APIRouter(prefix="/stocks")


@router.get("/{product_id}")
def get_stock(
    product_id: int,
    tenant_id: int = Depends(get_current_tenant),
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
