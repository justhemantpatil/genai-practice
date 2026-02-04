from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user
from app.services.budget_service import BudgetService
from app.schemas.budget import BudgetCreate, BudgetResponse
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=BudgetResponse)
async def create_budget(
    payload: BudgetCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    service = BudgetService(db)
    return await service.create_budget(payload, current_user)

@router.get("/", response_model=List[BudgetResponse])
async def get_budgets(
    wallet_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    service = BudgetService(db)
    return await service.get_budgets(wallet_id, current_user)
