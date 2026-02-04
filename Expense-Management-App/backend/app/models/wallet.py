from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from typing import List, TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.transaction import Transaction
    from app.models.budget import Budget

class WalletRole(str, enum.Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"

class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    currency: Mapped[str] = mapped_column(String, default="USD", nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="owned_wallets")
    members: Mapped[List["WalletMember"]] = relationship("WalletMember", back_populates="wallet", cascade="all, delete-orphan")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="wallet", cascade="all, delete-orphan")
    budgets: Mapped[List["Budget"]] = relationship("Budget", back_populates="wallet", cascade="all, delete-orphan")

class WalletMember(Base):
    __tablename__ = "wallet_members"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[WalletRole] = mapped_column(SQLEnum(WalletRole), default=WalletRole.MEMBER, nullable=False)

    # Relationships
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="wallet_memberships")
