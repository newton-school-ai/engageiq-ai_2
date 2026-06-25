from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.session import Session
    from src.models.user import User
    from src.models.engagement_log import EngagementLog

from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.engagement_log import EngagementState


class Nudge(Base):
    __tablename__ = "nudges"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    engagement_log_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("engagement_logs.id"), nullable=True
    )

    nudge_type: Mapped[str] = mapped_column(String, nullable=False)
    triggered_state: Mapped[EngagementState] = mapped_column(
        SQLEnum(EngagementState), nullable=False
    )
    effectiveness_delta: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    session: Mapped["Session"] = relationship("Session", back_populates="nudges")
    student: Mapped["User"] = relationship("User", back_populates="nudges")
    engagement_log: Mapped[Optional["EngagementLog"]] = relationship(
        "EngagementLog", back_populates="nudges"
    )
