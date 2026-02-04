from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog

class AuditRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, log: AuditLog) -> AuditLog:
        self.session.add(log)
        return log
    
    async def get_all(self, skip: int = 0, limit: int = 100):
        from sqlalchemy import select
        # Need to fix imports since select wasn't imported
        result = await self.session.execute(select(AuditLog).offset(skip).limit(limit).order_by(AuditLog.created_at.desc()))
        return list(result.scalars().all())
