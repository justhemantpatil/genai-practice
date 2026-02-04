from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.transaction import Transaction

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False) # INCOME or EXPENSE
    icon: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True) # Null for system default

    # Relationships
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="category")
