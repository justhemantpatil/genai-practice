from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from typing import Optional

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def create(self, user: User) -> User:
        self.session.add(user)
        # Commit usually happens in Service to allow transactions, but basic create can be here. 
        # We'll assume service handles commit or we do flush here.
        # Ideally, repository just adds, service commits. But for simple flow, we can flush.
        # Let's keep commit in Service for unit of work pattern, or here. 
        # If we want ID back immediately, we need flush/commit.
        # I'll rely on service to commit.
        return user
