from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.budget_repo import BudgetRepository
from app.repositories.wallet_repo import WalletRepository
from app.schemas.budget import BudgetCreate
from app.models.budget import Budget
from app.models.wallet import WalletRole
from app.models.user import User

class BudgetService:
    def __init__(self, session: AsyncSession):
        self.repo = BudgetRepository(session)
        self.wallet_repo = WalletRepository(session)
        self.session = session

    async def create_budget(self, budget_in: BudgetCreate, current_user: User) -> Budget:
        role = await self.wallet_repo.get_user_role(budget_in.wallet_id, current_user.id)
        if not role or role == WalletRole.VIEWER:
             raise HTTPException(status_code=403, detail="Not authorized to manage budgets")

        budget = Budget(
            amount=budget_in.amount,
            start_date=budget_in.start_date,
            end_date=budget_in.end_date,
            wallet_id=budget_in.wallet_id,
            category_id=budget_in.category_id
        )
        created = await self.repo.create(budget)
        await self.session.commit()
        await self.session.refresh(created)
        return created
    
    async def get_budgets(self, wallet_id: int, current_user: User):
        role = await self.wallet_repo.get_user_role(wallet_id, current_user.id)
        if not role:
             raise HTTPException(status_code=403, detail="Not authorized")
        return await self.repo.get_by_wallet(wallet_id)
