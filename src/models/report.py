from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.models.session import Session
    from src.models.user import User

from sqlalchemy import JSON, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("sessions.id"), nullable=True
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    report_type: Mapped[str] = mapped_column(String, nullable=False)
    content_json: Mapped[dict] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    session: Mapped[Optional["Session"]] = relationship(
        "Session", back_populates="reports"
    )
    user: Mapped[Optional["User"]] = relationship("User", back_populates="reports")
