from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.middleware.auth import get_current_user
from src.config.database import get_db
from src.models.course import CourseEnrollment
from src.models.user import User

router = APIRouter(
    prefix="/api/courses",
    tags=["Courses"],
)


@router.post("/{course_id}/enroll")
async def enroll_course(
    course_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == int(current_user["sub"])).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Only students can enroll",
        )

    enrollment = (
        db.query(CourseEnrollment)
        .filter(
            CourseEnrollment.course_id == course_id,
            CourseEnrollment.user_id == user.id,
        )
        .first()
    )

    if enrollment:
        raise HTTPException(
            status_code=400,
            detail="Already enrolled",
        )

    enrollment = CourseEnrollment(
        course_id=course_id,
        user_id=user.id,
    )

    db.add(enrollment)
    db.commit()

    return {
        "message": "Enrollment successful",
    }
