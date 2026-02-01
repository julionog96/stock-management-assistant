from fastapi import Header, HTTPException


def get_current_tenant(
    x_tenant_id: int = Header(...)
) -> int:
    if not x_tenant_id:
        raise HTTPException(status_code=401)

    return x_tenant_id
