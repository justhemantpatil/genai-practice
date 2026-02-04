from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.category_repo import CategoryRepository
from app.schemas.category import CategoryCreate
from app.models.category import Category
from app.models.user import User

class CategoryService:
    def __init__(self, session: AsyncSession):
        self.repo = CategoryRepository(session)
        self.session = session

    async def create_category(self, category_in: CategoryCreate, current_user: User) -> Category:
        category = Category(
            name=category_in.name,
            type=category_in.type,
            icon=category_in.icon,
            user_id=current_user.id
        )
        created = await self.repo.create(category)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def get_categories(self, current_user: User):
        return await self.repo.get_by_user(current_user.id)
