from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.budget import Budget
from typing import List

class BudgetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, budget: Budget) -> Budget:
        self.session.add(budget)
        return budget
    
    async def get_by_wallet(self, wallet_id: int) -> List[Budget]:
        result = await self.session.execute(select(Budget).where(Budget.wallet_id == wallet_id))
        return list(result.scalars().all())
