from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.middleware.auth import get_current_user
from src.api.schemas.user import OnboardingRequest, UserResponse
from src.config.database import get_db
from src.models.user import User

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == int(current_user["sub"])).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.post("/onboarding", response_model=UserResponse)
async def complete_onboarding(
    request: OnboardingRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == int(current_user["sub"])).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user.role = request.role
    user.privacy_mode = request.privacy_mode

    db.commit()
    db.refresh(user)

    return user
