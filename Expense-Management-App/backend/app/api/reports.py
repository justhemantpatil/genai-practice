from typing import Annotated, Dict
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user
from app.services.report_service import ReportService
from app.models.user import User

router = APIRouter()

@router.get("/monthly", response_model=Dict[str, float])
async def get_monthly_summary(
    wallet_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    month: int = Query(..., ge=1, le=12),
    year: int = Query(...),
    current_user: User = Depends(get_current_user)
):
    service = ReportService(db)
    return await service.get_monthly_summary(wallet_id, current_user, month, year)
