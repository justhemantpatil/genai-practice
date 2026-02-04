from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User
from app.utils.password import get_password_hash

class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)
        self.session = session

    async def create_user(self, user_in: UserCreate) -> User:
        user = await self.repo.get_by_email(user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this email already exists in the system.",
            )
        
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            is_active=user_in.is_active
        )
        created_user = await self.repo.create(db_user)
        # Commit to generate ID and save
        await self.session.commit()
        await self.session.refresh(created_user)
        return created_user

    async def get_user_by_email(self, email: str) -> User:
        return await self.repo.get_by_email(email)

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.repo.get_by_id(user_id)
