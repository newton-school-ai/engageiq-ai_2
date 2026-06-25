from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Boolean, DateTime, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from src.config.settings import UserRole, PrivacyMode

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column("password", String, nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False)
    privacy_mode: Mapped[PrivacyMode] = mapped_column(SQLEnum(PrivacyMode), nullable=False)

    avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    google_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    taught_courses: Mapped[List["Course"]] = relationship(
        "Course", back_populates="teacher", cascade="all, delete-orphan"
    )
    enrollments: Mapped[List["CourseEnrollment"]] = relationship(
        "CourseEnrollment", back_populates="student", cascade="all, delete-orphan"
    )
    engagement_logs: Mapped[List["EngagementLog"]] = relationship(
        "EngagementLog", back_populates="student", cascade="all, delete-orphan"
    )
    nudges: Mapped[List["Nudge"]] = relationship(
        "Nudge", back_populates="student", cascade="all, delete-orphan"
    )
    reports: Mapped[List["Report"]] = relationship(
        "Report", back_populates="user", cascade="all, delete-orphan"
    )
