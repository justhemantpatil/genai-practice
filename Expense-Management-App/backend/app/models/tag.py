from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.user import User

transaction_tags = Table(
    "transaction_tags",
    Base.metadata,
    Column("transaction_id", ForeignKey("transactions.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True) # User specific tags or system wide if null

    # Relationships
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", secondary=transaction_tags, back_populates="tags")
