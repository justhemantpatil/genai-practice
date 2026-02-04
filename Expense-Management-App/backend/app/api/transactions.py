from typing import Annotated, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user
from app.services.transaction_service import TransactionService
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    payload: TransactionCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    service = TransactionService(db)
    return await service.create_transaction(payload, current_user)

@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    wallet_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    current_user: User = Depends(get_current_user)
):
    service = TransactionService(db)
    return await service.get_transactions(wallet_id, current_user, skip, limit)
