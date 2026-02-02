from dataclasses import dataclass
from typing import Dict, Any

'''
Contexto do agente.
Será utilizado para passar informações para o agente.
'''


@dataclass
class AgentContext:
    tenant_id: int
    payload: Dict[str, Any]
