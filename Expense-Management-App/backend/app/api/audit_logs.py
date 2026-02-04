from typing import Annotated, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user
from app.services.audit_service import AuditService
from app.models.user import User
from app.schemas.audit_log import AuditLogResponse

router = APIRouter()

@router.get("/", response_model=List[AuditLogResponse])
async def get_audit_logs(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    current_user: User = Depends(get_current_user)
):
    # Depending on requirements, only admin might see all logs, or user sees their own.
    # For now, let's assume superuser or basic access for demo.
    if not current_user.is_superuser:
         # Maybe restrict to own actions? 
         # Simple implementation: return all for now or check is_superuser
         pass 
    
    service = AuditService(db)
    return await service.get_logs(skip, limit)
