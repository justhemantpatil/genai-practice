from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryResponse
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=CategoryResponse)
async def create_category(
    payload: CategoryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    service = CategoryService(db)
    return await service.create_category(payload, current_user)

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    service = CategoryService(db)
    return await service.get_categories(current_user)
