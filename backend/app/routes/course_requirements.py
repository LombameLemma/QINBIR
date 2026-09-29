from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.course_requirement import CourseRequirement
from app.models.course import Course
from app.models.student_section import StudentSection
from app.models.lecturer import Lecturer


router = APIRouter(
    prefix="/course-requirements",
    tags=["Course Requirements"]
)


class CourseRequirementCreate(BaseModel):
    course_id: int
    student_section_id: int
    lecturer_id: int
    sessions_per_week: int = 2
    long_session_hours: int = 2
    short_session_hours: int = 1


@router.get("/")
def get_course_requirements(db: Session = Depends(get_db)):
    return db.query(CourseRequirement).all()


@router.post("/")
def create_course_requirement(
    requirement: CourseRequirementCreate,
    db: Session = Depends(get_db)
):
    course = (
        db.query(Course)
        .filter(Course.id == requirement.course_id)
        .first()
    )

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    section = (
        db.query(StudentSection)
        .filter(
            StudentSection.id == requirement.student_section_id
        )
        .first()
    )

    if not section:
        raise HTTPException(
            status_code=404,
            detail="Student section not found"
        )

    lecturer = (
        db.query(Lecturer)
        .filter(Lecturer.id == requirement.lecturer_id)
        .first()
    )

    if not lecturer:
        raise HTTPException(
            status_code=404,
            detail="Lecturer not found"
        )

    new_requirement = CourseRequirement(
        course_id=requirement.course_id,
        student_section_id=requirement.student_section_id,
        lecturer_id=requirement.lecturer_id,
        sessions_per_week=requirement.sessions_per_week,
        long_session_hours=requirement.long_session_hours,
        short_session_hours=requirement.short_session_hours
    )

    db.add(new_requirement)
    db.commit()
    db.refresh(new_requirement)

    return new_requirement