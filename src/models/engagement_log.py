import enum
from datetime import datetime
from typing import List
from sqlalchemy import Float, Integer, DateTime, ForeignKey, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base


class EngagementState(str, enum.Enum):
    ENGAGED = "engaged"
    PASSIVE = "passive"
    DISTRACTED = "distracted"
    DROWSY = "drowsy"
    CONFUSED = "confused"


class EngagementLog(Base):
    __tablename__ = "engagement_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    engagement_score: Mapped[float] = mapped_column(Float, nullable=False)
    state: Mapped[EngagementState] = mapped_column(SQLEnum(EngagementState), nullable=False)

    drowsiness_count: Mapped[int] = mapped_column(Integer, default=0)
    negative_expression_count: Mapped[int] = mapped_column(Integer, default=0)
    distracted_count: Mapped[int] = mapped_column(Integer, default=0)
    phone_detected_count: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    session: Mapped["Session"] = relationship("Session", back_populates="engagement_logs")
    student: Mapped["User"] = relationship("User", back_populates="engagement_logs")
    nudges: Mapped[List["Nudge"]] = relationship("Nudge", back_populates="engagement_log")
