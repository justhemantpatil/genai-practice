from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    username: str
    password: str
    is_admin: bool = False

class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    is_admin: bool

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: str

class LoginRequest(BaseModel):
    username: str
    password: str


class NoteCreate(BaseModel):
    title: str
    content: str
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True
