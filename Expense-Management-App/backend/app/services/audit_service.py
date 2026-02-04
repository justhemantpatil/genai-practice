from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.audit_repo import AuditRepository
from app.models.audit_log import AuditLog
from typing import Optional

class AuditService:
    def __init__(self, session: AsyncSession):
        self.repo = AuditRepository(session)
        self.session = session

    async def log_action(self, action: str, entity_type: str, entity_id: str, user_id: Optional[int] = None, details: Optional[str] = None, ip_address: Optional[str] = None):
        log = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            details=details,
            ip_address=ip_address
        )
        await self.repo.create(log)
        # We might commit here or let the main transaction handle it. 
        # Audit logs often should be committed even if main transaction fails? No, usually same transaction.
        # If we want independent logging, we need separate session. 
        # For this exercise, same session is fine.

    async def get_logs(self, skip: int = 0, limit: int = 100):
        return await self.repo.get_all(skip, limit)
