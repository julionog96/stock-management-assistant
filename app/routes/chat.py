from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.agent.context import AgentContext
from app.agent.orchestrator import AgentOrchestrator
from app.auth.auth import get_current_tenant

router = APIRouter(prefix="/chat")


@router.post("/", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    tenant_id: int = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    context = AgentContext(
        tenant_id=tenant_id,
        payload={}
    )

    agent = AgentOrchestrator(db)

    response = agent.handle_chat_message(
        context=context,
        message=payload.message
    )

    return ChatResponse(response=response)
