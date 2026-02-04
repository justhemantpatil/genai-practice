from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BudgetBase(BaseModel):
    amount: float
    start_date: datetime
    end_date: datetime
    category_id: Optional[int] = None

class BudgetCreate(BudgetBase):
    wallet_id: int

class BudgetResponse(BudgetBase):
    id: int
    wallet_id: int

    class Config:
        from_attributes = True
