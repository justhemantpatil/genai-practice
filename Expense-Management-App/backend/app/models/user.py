from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.wallet import Wallet, WalletMember
    from app.models.audit_log import AuditLog

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    owned_wallets: Mapped[List["Wallet"]] = relationship("Wallet", back_populates="owner", cascade="all, delete-orphan")
    wallet_memberships: Mapped[List["WalletMember"]] = relationship("WalletMember", back_populates="user", cascade="all, delete-orphan")
    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLog", back_populates="user")
