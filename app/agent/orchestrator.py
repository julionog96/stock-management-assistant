from sqlalchemy.orm import Session

from app.models.stock import Stock

from app.agent.context import AgentContext
from app.agent.decisions import AgentDecision, llm_decision

from app.agent.tools import AgentTools


class AgentOrchestrator:

    def __init__(self, db: Session):
        self.db = db
        self.tools = AgentTools(db)

    def _handle_stock_question(
        self,
        context: AgentContext
    ) -> str:
        """
        Simula uma consulta de estoque via agente.
        """
        stocks = (
            self.db.query(Stock)
            .filter(Stock.tenant_id == context.tenant_id)
            .all()
        )

        if not stocks:
            return "Não há informações de estoque disponíveis."

        lines = []
        for stock in stocks:

            lines.append(
                f"{stock.product}: "
                f"{stock.quantity} unidades "
                f"(mínimo: {stock.minimum_quantity})"
            )

        return "\n".join(lines)

    def handle_stock_below_threshold(
        self,
        context: AgentContext,
        product_id: int,
        current_quantity: int,
        minimum_quantity: int
    ) -> None:
        """
        Fluxo proativo: chamado pelo cron job.
        Valida se o estoque está abaixo do limite mínimo e toma uma decisão.
        """

        decision = llm_decision(
            current_quantity=current_quantity,
            minimum_quantity=minimum_quantity
        )

        if decision == AgentDecision.REFILL:
            self.tools.refill_stock(
                tenant_id=context.tenant_id,
                product_id=product_id,
                quantity=minimum_quantity * 2 
            )

        elif decision == AgentDecision.NOTIFY:
            self.tools.notify_manager(
                tenant_id=context.tenant_id,
                product_id=product_id,
                message="Stock below minimum threshold"
            )

        elif decision == AgentDecision.IGNORE:
            # Por enquanto nenhuma ação necessária
            pass

    def handle_chat_message(self, context: AgentContext, message: str) -> str:
        """
        Fluxo conversacional: responde perguntas do usuário.
        """

        # mock de interpretação da intenção
        normalized = message.lower()

        if "estoque" in normalized:
            return self._handle_stock_question(context)

        return "Não entendi sua pergunta. Tente perguntar sobre o estoque."
