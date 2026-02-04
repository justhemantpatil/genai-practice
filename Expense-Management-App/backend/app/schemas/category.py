from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    type: str
    icon: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
