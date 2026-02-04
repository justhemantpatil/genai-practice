from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.category import Category
from typing import List, Optional

class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, category: Category) -> Category:
        self.session.add(category)
        return category

    async def get_by_user(self, user_id: int) -> List[Category]:
        # Get system categories (user_id is None) and user specific categories
        result = await self.session.execute(
            select(Category).where((Category.user_id == user_id) | (Category.user_id == None))
        )
        return list(result.scalars().all())

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        result = await self.session.execute(select(Category).where(Category.id == category_id))
        return result.scalars().first()
