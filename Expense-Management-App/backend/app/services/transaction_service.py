from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.wallet_repo import WalletRepository
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.models.transaction import Transaction
from app.models.wallet import WalletRole
from app.models.user import User
from app.services.audit_service import AuditService

class TransactionService:
    def __init__(self, session: AsyncSession):
        self.repo = TransactionRepository(session)
        self.wallet_repo = WalletRepository(session)
        self.audit_service = AuditService(session)
        self.session = session

    async def create_transaction(self, transaction_in: TransactionCreate, current_user: User) -> Transaction:
        # Check specific wallet permission
        role = await self.wallet_repo.get_user_role(transaction_in.wallet_id, current_user.id)
        if not role or role == WalletRole.VIEWER:
            raise HTTPException(status_code=403, detail="Not authorized to create transactions in this wallet")

        transaction = Transaction(
            amount=transaction_in.amount,
            description=transaction_in.description,
            type=transaction_in.type,
            date=transaction_in.date,
            wallet_id=transaction_in.wallet_id,
            category_id=transaction_in.category_id
        )
        
        created_txn = await self.repo.create(transaction)
        await self.session.commit()
        await self.session.refresh(created_txn)
        
        await self.audit_service.log_action(
            action="CREATE_TRANSACTION",
            entity_type="TRANSACTION",
            entity_id=str(created_txn.id),
            user_id=current_user.id,
            details=f"Created {transaction_in.type} transaction of {transaction_in.amount}"
        )
        return created_txn

    async def get_transactions(self, wallet_id: int, current_user: User, skip: int = 0, limit: int = 100):
        role = await self.wallet_repo.get_user_role(wallet_id, current_user.id)
        if not role:
             raise HTTPException(status_code=403, detail="Not authorized to access this wallet")
        
        return await self.repo.get_by_wallet(wallet_id, skip, limit)
