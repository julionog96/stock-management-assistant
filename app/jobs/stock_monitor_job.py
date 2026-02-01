from sqlalchemy.orm import Session
import random

from app.database import SessionLocal
from app.models.stock import Stock
from app.services.treshold_service import ThresholdService


def forecast_minimum(stock: Stock) -> int:
    """
    Simula um motor de previsão de séries temporais.
    Em produção seria substituido por uma ferramenta de previsão..
    """
    base = max(1, stock.quantity // 2)
    variation = random.randint(0, 5)
    return base + variation


def mock_agent_decision(
    tenant_id: int,
    product_id: int,
    current_quantity: int,
    minimum_quantity: int
) -> str:
    """
    Simula a decisão de um agente LLM e retorna qual ação deve ser executada.
    A ideia é que em produção seja utilizada uma LLM de fato.
    """
    if current_quantity < minimum_quantity:
        return "REFILL"

    return "IGNORE"


def run_stock_monitor_job():
    print("Running stock monitoring job...")

    db: Session = SessionLocal()

    try:
        stocks = db.query(Stock).all()

        for stock in stocks:
            minimum = forecast_minimum(stock)

            ThresholdService.update_threshold(
                db=db,
                tenant_id=stock.tenant_id,
                product_id=stock.product_id,
                minimum_quantity=minimum
            )

            if stock.quantity < minimum:
                decision = mock_agent_decision(
                    tenant_id=stock.tenant_id,
                    product_id=stock.product_id,
                    current_quantity=stock.quantity,
                    minimum_quantity=minimum
                )

                if decision == "REFILL":
                    print(
                        f"Tenant {stock.tenant_id} | "
                        f"Product {stock.product_id} | "
                        f"Stock {stock.quantity} < Minimum {minimum} → REFILL"
                    )
                else:
                    print(
                        f"Tenant {stock.tenant_id} | "
                        f"Product {stock.product_id} | "
                        f"Decision: IGNORE"
                    )

        print("Stock monitoring job finished.")

    finally:
        db.close()


if __name__ == "__main__":
    run_stock_monitor_job()
