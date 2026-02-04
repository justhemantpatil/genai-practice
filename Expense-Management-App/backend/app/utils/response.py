from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    status: str
    data: Optional[T] = None
    message: Optional[str] = None
