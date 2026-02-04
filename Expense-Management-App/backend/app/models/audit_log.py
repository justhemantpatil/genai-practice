from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    action: Mapped[str] = mapped_column(String, nullable=False)
    entity_type: Mapped[str] = mapped_column(String, nullable=False) 
    entity_id: Mapped[str] = mapped_column(String, nullable=True) # Storing ID as string for flexibility
    details: Mapped[str] = mapped_column(String, nullable=True)
    ip_address: Mapped[str] = mapped_column(String, nullable=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="audit_logs")
