from typing import Annotated
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user
from app.services.wallet_service import WalletService
from app.models.wallet import WalletRole
from app.models.user import User
from pydantic import BaseModel, EmailStr

router = APIRouter()

class AddMemberRequest(BaseModel):
    email: EmailStr
    role: WalletRole

@router.post("/{wallet_id}/members")
async def add_member(
    wallet_id: int,
    payload: AddMemberRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    service = WalletService(db)
    return await service.add_wallet_member(wallet_id, payload.email, payload.role, current_user)
