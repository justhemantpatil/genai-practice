from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.transaction import Transaction
from typing import List, Optional

class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        return transaction

    async def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        result = await self.session.execute(select(Transaction).where(Transaction.id == transaction_id))
        return result.scalars().first()

    async def get_by_wallet(self, wallet_id: int, skip: int = 0, limit: int = 100) -> List[Transaction]:
        result = await self.session.execute(
            select(Transaction).where(Transaction.wallet_id == wallet_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, transaction: Transaction):
        # Transaction is tracked by session, just needs commit in service
        pass

    async def delete(self, transaction: Transaction):
        await self.session.delete(transaction)
