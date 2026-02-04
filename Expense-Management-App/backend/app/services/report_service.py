from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.transaction import Transaction
from app.repositories.wallet_repo import WalletRepository
from app.models.user import User
from fastapi import HTTPException

class ReportService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.wallet_repo = WalletRepository(session)

    async def get_monthly_summary(self, wallet_id: int, current_user: User, month: int, year: int):
        role = await self.wallet_repo.get_user_role(wallet_id, current_user.id)
        if not role:
            raise HTTPException(status_code=403, detail="Not authorized")

        # Aggregate income and expense
        # Query: Filter by wallet, month, year. Sum amount grouping by type.
        stmt = select(Transaction.type, func.sum(Transaction.amount)).where(
            Transaction.wallet_id == wallet_id,
            func.extract('month', Transaction.date) == month,
            func.extract('year', Transaction.date) == year
        ).group_by(Transaction.type)

        result = await self.session.execute(stmt)
        data = result.all()
        
        summary = {"INCOME": 0.0, "EXPENSE": 0.0}
        for type_, total in data:
            summary[type_] = total or 0.0
            
        return summary
