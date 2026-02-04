from sqlalchemy import Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.wallet import Wallet
    from app.models.category import Category

class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True) # Null for total wallet budget

    # Relationships
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="budgets")
    category: Mapped["Category"] = relationship(foreign_keys=[category_id])
