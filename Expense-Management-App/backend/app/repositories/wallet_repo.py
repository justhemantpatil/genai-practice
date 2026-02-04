from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.wallet import Wallet, WalletMember, WalletRole
from typing import List, Optional

class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, wallet: Wallet) -> Wallet:
        self.session.add(wallet)
        return wallet

    async def get_by_id(self, wallet_id: int) -> Optional[Wallet]:
        result = await self.session.execute(select(Wallet).where(Wallet.id == wallet_id))
        return result.scalars().first()

    async def get_by_owner(self, user_id: int) -> List[Wallet]:
        result = await self.session.execute(select(Wallet).where(Wallet.owner_id == user_id))
        return list(result.scalars().all())

    async def add_member(self, member: WalletMember) -> WalletMember:
        self.session.add(member)
        return member

    async def get_members(self, wallet_id: int) -> List[WalletMember]:
        result = await self.session.execute(select(WalletMember).where(WalletMember.wallet_id == wallet_id))
        return list(result.scalars().all())

    async def get_wallets_for_user(self, user_id: int) -> List[Wallet]:
        # Join WalletMember and Wallet
        stmt = select(Wallet).join(WalletMember).where(WalletMember.user_id == user_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_user_role(self, wallet_id: int, user_id: int) -> Optional[WalletRole]:
        # Check ownership first
        wallet = await self.get_by_id(wallet_id)
        if wallet and wallet.owner_id == user_id:
            return WalletRole.OWNER
        
        result = await self.session.execute(
            select(WalletMember.role).where(WalletMember.wallet_id == wallet_id, WalletMember.user_id == user_id)
        )
        return result.scalars().first()
