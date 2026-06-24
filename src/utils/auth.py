"""Session token verification.

TODO(#6): This is a placeholder until the Google OAuth + JWT session work
in issue #6 lands. The verification contract here (decode with
``settings.secret_key``, require ``sub`` + unexpired ``exp``) is expected
to match the tokens issued by #6 once that's merged. If #6 ends up using a
different claim layout, update ``decode_session_token`` accordingly --
callers (e.g. the websocket endpoint) should not need to change.
"""
from __future__ import annotations

import jwt
from jwt import PyJWTError

from src.config.settings import settings

ALGORITHM = "HS256"


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