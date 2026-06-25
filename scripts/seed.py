import sys
import os
import random
from datetime import datetime, timedelta

# Add the project root to the python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings, UserRole, PrivacyMode
from src.models import (
    Base,
    User,
    Course,
    CourseEnrollment,
    Session,
    EngagementLog,
    EngagementState,
    Nudge,
    Report,
)


def seed_database():
    print(f"Connecting to database: {settings.database_url}")
    engine = create_engine(settings.database_url)

    # Clear existing data and recreate tables to ensure a clean slate
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        print("Seeding Users...")
        # Create 2 Teachers
        teachers = [
            User(
                name=f"Teacher {i}",
                email=f"teacher{i}@engageiq.com",
                password="password123",
                role=UserRole.TEACHER,
                privacy_mode=PrivacyMode.LOCAL_ONLY,
                google_id=f"google_teacher_{i}",
            )
            for i in range(1, 3)
        ]
        session.add_all(teachers)
        session.commit()

        # Create 10 Students
        students = [
            User(
                name=f"Student {i}",
                email=f"student{i}@engageiq.com",
                password="password123",
                role=UserRole.STUDENT,
                privacy_mode=PrivacyMode.SHARE_WITH_TEACHER,
                google_id=f"google_student_{i}",
            )
            for i in range(1, 11)
        ]
        session.add_all(students)
        session.commit()

        print("Seeding Courses...")
        courses = [
            Course(
                teacher_id=teachers[0].id,
                name="Introduction to Python",
                code="CS101",
                description="Learn the basics of Python programming.",
            ),
            Course(
                teacher_id=teachers[0].id,
                name="Data Structures",
                code="CS201",
                description="Arrays, linked lists, trees, and graphs.",
            ),
            Course(
                teacher_id=teachers[1].id,
                name="Machine Learning",
                code="CS301",
                description="Supervised and unsupervised learning techniques.",
            ),
        ]
        session.add_all(courses)
        session.commit()

        print("Seeding Enrollments...")
        for student in students:
            # Enroll in 1 to 3 random courses
            for course in courses[: random.randint(1, 3)]:
                session.add(CourseEnrollment(course_id=course.id, user_id=student.id))
        session.commit()

        print("Seeding Sessions...")
        now = datetime.now()
        sessions = [
            Session(
                course_id=courses[0].id,
                title="Python Basics 1",
                start_time=now - timedelta(days=2),
                end_time=now - timedelta(days=2, hours=-1),
                status="completed",
            ),
            Session(
                course_id=courses[0].id,
                title="Python Basics 2",
                start_time=now - timedelta(days=1),
                end_time=now - timedelta(days=1, hours=-1),
                status="completed",
            ),
            Session(
                course_id=courses[1].id,
                title="Arrays and Lists",
                start_time=now - timedelta(hours=5),
                end_time=now - timedelta(hours=4),
                status="completed",
            ),
            Session(
                course_id=courses[1].id,
                title="Trees",
                start_time=now,
                status="active",
            ),
            Session(
                course_id=courses[2].id,
                title="Linear Regression",
                start_time=now + timedelta(days=1),
                status="scheduled",
            ),
        ]
        session.add_all(sessions)
        session.commit()

        print("Seeding Engagement Logs & Nudges...")
        past_sessions = [s for s in sessions if s.status in ["completed", "active"]]
        states = list(EngagementState)

        for s in past_sessions:
            enrolled_students = [
                e.student
                for e in session.query(CourseEnrollment).filter_by(course_id=s.course_id).all()
            ]
            for student in enrolled_students:
                # 5 logs per student per session
                for i in range(5):
                    log_time = s.start_time + timedelta(minutes=i * 10)
                    state = random.choice(states)

                    is_bad_state = state in [
                        EngagementState.DISTRACTED,
                        EngagementState.DROWSY,
                        EngagementState.CONFUSED,
                    ]

                    log = EngagementLog(
                        session_id=s.id,
                        user_id=student.id,
                        timestamp=log_time,
                        engagement_score=random.uniform(0.1, 1.0),
                        state=state,
                        drowsiness_count=random.randint(1, 5) if state == EngagementState.DROWSY else 0,
                        distracted_count=random.randint(1, 5) if state == EngagementState.DISTRACTED else 0,
                        negative_expression_count=random.randint(1, 5) if is_bad_state else 0,
                        phone_detected_count=random.randint(0, 2) if state == EngagementState.DISTRACTED else 0,
                    )
                    session.add(log)
                    session.commit()

                    # Occasionally trigger a nudge for bad states
                    if state in [EngagementState.DISTRACTED, EngagementState.DROWSY]:
                        nudge = Nudge(
                            session_id=s.id,
                            user_id=student.id,
                            engagement_log_id=log.id,
                            nudge_type="pop-up",
                            triggered_state=state,
                            effectiveness_delta=random.uniform(-0.2, 0.8),
                        )
                        session.add(nudge)

        print("Seeding Reports...")
        completed_sessions = [s for s in sessions if s.status == "completed"]
        for s in completed_sessions:
            enrolled_students = [
                e.student
                for e in session.query(CourseEnrollment).filter_by(course_id=s.course_id).all()
            ]
            for student in enrolled_students:
                report = Report(
                    session_id=s.id,
                    user_id=student.id,
                    report_type="session_summary",
                    content_json={
                        "avg_engagement_score": round(random.uniform(0.4, 0.95), 2),
                        "total_logs": 5,
                        "distracted_count": random.randint(0, 3),
                        "drowsy_count": random.randint(0, 2),
                        "nudges_triggered": random.randint(0, 2),
                        "session_title": s.title,
                    },
                )
                session.add(report)
        session.commit()

        print("Database seeded successfully with the updated ERD schema!")


if __name__ == "__main__":
    seed_database()
