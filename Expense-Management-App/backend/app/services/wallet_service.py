from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.wallet_repo import WalletRepository
from app.schemas.wallet import WalletCreate, WalletUpdate
from app.models.wallet import Wallet, WalletMember, WalletRole
from app.models.user import User
from app.services.audit_service import AuditService

class WalletService:
    def __init__(self, session: AsyncSession):
        self.repo = WalletRepository(session)
        self.audit_service = AuditService(session)
        self.session = session

    async def create_wallet(self, wallet_in: WalletCreate, current_user: User) -> Wallet:
        wallet = Wallet(
            name=wallet_in.name,
            description=wallet_in.description,
            currency=wallet_in.currency,
            owner_id=current_user.id
        )
        created_wallet = await self.repo.create(wallet)
        await self.session.flush() # Flush to get ID

        # Add owner as admin member implicitly or just rely on owner_id? 
        # Usually good to add to members too for uniform queries.
        member = WalletMember(wallet_id=created_wallet.id, user_id=current_user.id, role=WalletRole.OWNER)
        await self.repo.add_member(member)

        await self.session.commit()
        await self.session.refresh(created_wallet)
        
        await self.audit_service.log_action(
            action="CREATE_WALLET",
            entity_type="WALLET",
            entity_id=str(created_wallet.id),
            user_id=current_user.id,
            details=f"Created wallet {created_wallet.name}"
        )
        
        return created_wallet

    async def get_my_wallets(self, current_user: User):
        return await self.repo.get_wallets_for_user(current_user.id)
    
    async def get_wallet(self, wallet_id: int, current_user: User) -> Wallet:
        role = await self.repo.get_user_role(wallet_id, current_user.id)
        if not role:
             raise HTTPException(status_code=403, detail="Not authorized to access this wallet")
        
        wallet = await self.repo.get_by_id(wallet_id)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        return wallet
        
    async def add_wallet_member(self, wallet_id: int, user_email: str, role: WalletRole, current_user: User):
        # Check permissions
        current_role = await self.repo.get_user_role(wallet_id, current_user.id)
        if current_role not in [WalletRole.OWNER, WalletRole.ADMIN]:
            raise HTTPException(status_code=403, detail="Not authorized to add members")

        # Find user to add
        from app.repositories.user_repo import UserRepository
        user_repo = UserRepository(self.session)
        user_to_add = await user_repo.get_by_email(user_email)
        if not user_to_add:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Check if already member
        existing_role = await self.repo.get_user_role(wallet_id, user_to_add.id)
        if existing_role:
            raise HTTPException(status_code=400, detail="User is already a member")

        member = WalletMember(wallet_id=wallet_id, user_id=user_to_add.id, role=role)
        await self.repo.add_member(member)
        await self.session.commit()
        
        await self.audit_service.log_action(
            action="ADD_MEMBER",
            entity_type="WALLET",
            entity_id=str(wallet_id),
            user_id=current_user.id,
            details=f"Added {user_email} as {role}"
        )
        return member
