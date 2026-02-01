from sqlalchemy.orm import Session
from app.services.stock_service import StockService

'''
define o contrato das ferramentas que o agente pode utilizar.
'''


class AgentTools:

    def __init__(self, db: Session):
        self.db = db

    def refill_stock(self, tenant_id: int, product_id: int, quantity: int):
        """
        Função que executa reabastecimento de estoque.
        """
        if not tenant_id:
            raise ValueError("Tenant ID is required")
        if not product_id:
            raise ValueError("Product ID is required")
        if not quantity:
            raise ValueError("Quantity is required")

        StockService.update_stock(
            db=self.db,
            tenant_id=tenant_id,
            product_id=product_id,
            quantity=quantity
        )

    def notify_manager(self, tenant_id: int, product_id: int, message: str):
        """
        Notifica o gerente sobre a situação do estoque.
        """
        print(
            f"Notify Tenant {tenant_id} | "
            f"Product {product_id}: {message}"
        )
