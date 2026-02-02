from sqlalchemy.orm import Session
import random

from app.database import SessionLocal
from app.models.stock import Stock
from app.services.stock_service import StockService
from app.agent.orchestrator import AgentOrchestrator
from app.agent.context import AgentContext


def forecast_minimum(stock: Stock) -> int:
    """
    Simula um motor de previsão de séries temporais.
    Em produção seria substituido por uma ferramenta de previsão..
    """
    base = max(1, stock.quantity // 2)
    variation = random.randint(0, 5)
    return base + variation


def run_stock_monitor_job():
    print("Running stock monitoring job...")

    db: Session = SessionLocal()

    try:
        stocks = db.query(Stock).all()

        for stock in stocks:
            minimum = forecast_minimum(stock)
            agent = AgentOrchestrator(db)

            context = AgentContext(tenant_id=stock.tenant_id, payload={})

            # valida se o estoque está abaixo do limite mínimo
            agent.handle_stock_below_threshold(
                context=context,
                product_id=stock.product_id,
                current_quantity=stock.quantity,
                minimum_quantity=minimum
            )

            StockService().update_threshold(
                db=db,
                tenant_id=stock.tenant_id,
                product_id=stock.product_id,
                minimum_quantity=minimum
            )

        print("Stock monitoring job finished.")

    finally:
        db.close()


if __name__ == "__main__":
    run_stock_monitor_job()
