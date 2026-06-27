import httpx
from fastapi import APIRouter, Depends, HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from src.api.schemas.user import GoogleAuthRequest, TokenResponse
from src.config.database import get_db
from src.config.settings import settings
from src.models.user import User
from src.utils.auth import (create_access_token, create_refresh_token,
                            verify_token)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post("/google", response_model=TokenResponse)
async def google_login(
    request: GoogleAuthRequest,
    db: Session = Depends(get_db),
):
    """Authenticate user using Google OAuth."""

    tokens = await exchange_code_for_tokens(request.code)

    try:
        google_id_info = id_token.verify_oauth2_token(
            tokens["id_token"],
            requests.Request(),
            settings.google_client_id,
        )
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid Google ID token",
        )

    email = google_id_info["email"]

    user = (
        db.query(User)
        .filter((User.email == email) | (User.google_id == google_id_info["sub"]))
        .first()
    )
    if user is None:
        user = User(
            name=google_id_info.get("name"),
            email=email,
            google_id=google_id_info.get("sub"),
            avatar_url=google_id_info.get("picture"),
            auth_provider="google",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    else:
        if not user.google_id:
            user.google_id = google_id_info["sub"]

        user.avatar_url = google_id_info.get("picture")
        user.name = google_id_info.get("name")

        db.commit()
        db.refresh(user)

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": str(user.id),
        }
    )

    needs_onboarding = user.role is None or user.privacy_mode is None

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        needs_onboarding=needs_onboarding,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """Refresh JWT access token."""

    payload = verify_token(
        refresh_token,
        token_type="refresh",
    )

    access_token = create_access_token(
        {
            "sub": payload["sub"],
        }
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        needs_onboarding=False,
    )


async def exchange_code_for_tokens(code: str) -> dict:
    """Exchange Google authorization code for tokens."""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail="Google token exchange failed",
        )

    return response.json()
