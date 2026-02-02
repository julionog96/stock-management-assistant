from pydantic import BaseModel


class StockResponse(BaseModel):
    """Resposta do endpoint de estoque com dados da loja e do produto."""

    tenant_id: int
    tenant_name: str
    product_id: int
    product_name: str
    quantity: int
    minimum_quantity: int
