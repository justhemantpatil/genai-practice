from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from typing import List, TYPE_CHECKING
from app.models.wallet import WalletRole
import enum

if TYPE_CHECKING:
    from app.models.wallet import Wallet

class InviteStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class WalletInvite(Base):
    __tablename__ = "wallet_invites"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, index=True, nullable=False)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    role: Mapped[str] = mapped_column(String, default=WalletRole.MEMBER, nullable=False)
    status: Mapped[str] = mapped_column(String, default=InviteStatus.PENDING, nullable=False)
    token: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    # Relationships
    wallet: Mapped["Wallet"] = relationship("Wallet")
