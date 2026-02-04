from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user
from app.services.wallet_service import WalletService
from app.schemas.wallet import WalletCreate, WalletResponse
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=WalletResponse)
async def create_wallet(
    payload: WalletCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    service = WalletService(db)
    return await service.create_wallet(payload, current_user)

@router.get("/", response_model=List[WalletResponse])
async def get_wallets(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    service = WalletService(db)
    return await service.get_my_wallets(current_user)

@router.get("/{wallet_id}", response_model=WalletResponse)
async def get_wallet(
    wallet_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    service = WalletService(db)
    return await service.get_wallet(wallet_id, current_user)
