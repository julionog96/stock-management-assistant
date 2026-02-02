from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tenant import Tenant


def get_current_tenant(
    db: Session = Depends(get_db),
    x_tenant_id: int = Header(...)
) -> int:

    tenant = db.query(Tenant).filter(Tenant.id == x_tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=401)

    return tenant.id
