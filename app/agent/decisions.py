from enum import Enum

'''
define as decisões que o agente pode tomar.
'''


class AgentDecision(str, Enum):
    REFILL = "REFILL"
    NOTIFY = "NOTIFY"
    IGNORE = "IGNORE"


def llm_decision(
    current_quantity: int,
    minimum_quantity: int
) -> AgentDecision:
    """
    Simula uma decisão tomada por uma LLM.
    """
    if current_quantity < minimum_quantity:
        return AgentDecision.REFILL

    return AgentDecision.IGNORE
