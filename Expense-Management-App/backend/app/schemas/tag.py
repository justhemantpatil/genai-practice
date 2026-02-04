from pydantic import BaseModel
from typing import Optional, List

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
