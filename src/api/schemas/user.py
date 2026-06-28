"""Pydantic schemas for user authentication and onboarding."""

from pydantic import BaseModel, ConfigDict, EmailStr

from src.config.settings import PrivacyMode, UserRole


class GoogleAuthRequest(BaseModel):
    """Request body for Google OAuth login."""

    code: str


class OnboardingRequest(BaseModel):
    """Request body for first-time user onboarding."""

    role: UserRole
    privacy_mode: PrivacyMode


class UserResponse(BaseModel):
    """User profile returned to the frontend."""

    id: int
    name: str
    email: EmailStr
    role: UserRole
    privacy_mode: PrivacyMode
    avatar_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """JWT tokens returned after successful login."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
