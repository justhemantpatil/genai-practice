from pydantic import BaseModel
from typing import Optional, List
from app.models.wallet import WalletRole

class WalletBase(BaseModel):
    name: str
    description: Optional[str] = None
    currency: Optional[str] = "USD"

class WalletCreate(WalletBase):
    pass

class WalletUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None

class WalletMemberResponse(BaseModel):
    user_id: int
    role: WalletRole
    
    class Config:
        from_attributes = True

class WalletResponse(WalletBase):
    id: int
    owner_id: int
    # members: List[WalletMemberResponse] = [] # Optional to include

    class Config:
        from_attributes = True
