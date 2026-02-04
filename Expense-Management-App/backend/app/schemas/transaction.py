from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    description: Optional[str] = None
    type: str # INCOME or EXPENSE
    date: datetime = datetime.utcnow()
    category_id: Optional[int] = None

class TransactionCreate(TransactionBase):
    wallet_id: int # Explicitly needed if creating directly, or inferred from context

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    type: Optional[str] = None
    date: Optional[datetime] = None
    category_id: Optional[int] = None

class TransactionResponse(TransactionBase):
    id: int
    wallet_id: int

    class Config:
        from_attributes = True
