from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.stock_service import StockService
from app.auth.auth import get_current_tenant
from app.schemas.stock import StockResponse

router = APIRouter(prefix="/stocks")


@router.get("/{product_id}", response_model=StockResponse)
def get_stock(
    product_id: int,
    tenant_id: int = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    '''
    Retorna o estoque com detalhes do tenant e do produto.
    '''
    stock = StockService.get_stock_with_details(
        db=db,
        tenant_id=tenant_id,
        product_id=product_id
    )

    if not stock:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")

    return StockResponse(
        tenant_id=stock.tenant_id,
        tenant_name=stock.tenant.name,
        product_id=stock.product_id,
        product_name=stock.product.name,
        quantity=stock.quantity,
        minimum_quantity=stock.minimum_quantity,
    )
