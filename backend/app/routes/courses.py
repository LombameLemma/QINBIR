from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.course import Course
from app.models.program import Program


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


class CourseCreate(BaseModel):
    code: str
    name: str
    credit_hours: int
    program_id: int


@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()

    return courses


@router.post("/")
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    # Check that the program exists
    program = (
        db.query(Program)
        .filter(Program.id == course.program_id)
        .first()
    )

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    # Check for duplicate course code
    existing_course = (
        db.query(Course)
        .filter(Course.code == course.code)
        .first()
    )

    if existing_course:
        raise HTTPException(
            status_code=400,
            detail="Course code already exists"
        )

    # Check valid credit hours
    if course.credit_hours <= 0:
        raise HTTPException(
            status_code=400,
            detail="Credit hours must be greater than 0"
        )

    new_course = Course(
        code=course.code,
        name=course.name,
        credit_hours=course.credit_hours,
        program_id=course.program_id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course