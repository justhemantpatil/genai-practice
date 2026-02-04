from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from typing import TYPE_CHECKING, List
from datetime import datetime

if TYPE_CHECKING:
    from app.models.wallet import Wallet
    from app.models.category import Category
    from app.models.tag import Tag
    from typing import List

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False) # INCOME or EXPENSE (redundant if category has type, but good for quick access or transfers)
    
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True) # Nullable for transfers

    # Relationships
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="transactions")
    category: Mapped["Category"] = relationship("Category", back_populates="transactions")
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary="transaction_tags", back_populates="transactions")
