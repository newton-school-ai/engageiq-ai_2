"""Session token verification.

TODO(#6): This is a placeholder until the Google OAuth + JWT session work
in issue #6 lands. The verification contract here (decode with
``settings.secret_key``, require ``sub`` + unexpired ``exp``) is expected
to match the tokens issued by #6 once that's merged. If #6 ends up using a
different claim layout, update ``decode_session_token`` accordingly --
callers (e.g. the websocket endpoint) should not need to change.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt
from jwt import PyJWTError

from src.config.settings import settings

ALGORITHM = settings.jwt_algorithm


class InvalidSessionToken(Exception):
    """Raised when a session token is missing, malformed, expired, or invalid."""


def decode_session_token(token: str) -> dict:
    """Decode and validate a JWT session token.

    Args:
        token: The raw JWT string (no "Bearer " prefix expected).

    Returns:
        The decoded claims dict (expected to include at least "sub",
        the user/session identifier).

    Raises:
        InvalidSessionToken: If the token is missing, expired, or otherwise
            fails validation.
    """
    if not token:
        raise InvalidSessionToken("Missing session token")

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except PyJWTError as exc:
        raise InvalidSessionToken(f"Invalid session token: {exc}") from exc

    if "sub" not in payload:
        raise InvalidSessionToken("Session token missing 'sub' claim")

    return payload


def verify_session_token(token: str) -> str:
    """Validate a session token and return the subject (user/session id).

    Convenience wrapper around ``decode_session_token`` for callers that
    only need the subject claim.
    """
    payload = decode_session_token(token)
    return payload["sub"]


def create_access_token(data: dict) -> str:
    """Create a JWT access token."""

    payload = data.copy()
    now = datetime.now(timezone.utc)

    payload.update(
        {
            "iat": now,
            "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
            "type": "access",
        }
    )

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token."""

    payload = data.copy()
    now = datetime.now(timezone.utc)

    payload.update(
        {
            "iat": now,
            "exp": now + timedelta(days=settings.refresh_token_expire_days),
            "type": "refresh",
        }
    )

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def decode_token(token: str) -> dict:
    """Decode any JWT token."""
    return decode_session_token(token)


def verify_token(token: str, token_type: str = "access") -> dict:
    """Verify JWT type and validity."""

    payload = decode_token(token)

    if payload.get("type") != token_type:
        raise InvalidSessionToken("Invalid token type")

    return payload
