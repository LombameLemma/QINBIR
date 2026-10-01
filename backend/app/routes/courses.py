
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.course import Course
from app.models.program import Program
from app.models.program_course import ProgramCourse


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


# =========================================================
# REQUEST MODELS
# =========================================================

class CourseCreate(BaseModel):
    code: str
    name: str
    credit_hours: int


class ProgramCourseCreate(BaseModel):
    program_id: int


# =========================================================
# GET ALL COURSES
# =========================================================

@router.get("/")
def get_courses(
    db: Session = Depends(get_db)
):

    courses = db.query(Course).all()

    result = []

    for course in courses:

        relationships = (
            db.query(ProgramCourse)
            .filter(
                ProgramCourse.course_id == course.id
            )
            .all()
        )

        programs = []

        for relationship in relationships:

            program = (
                db.query(Program)
                .filter(
                    Program.id == relationship.program_id
                )
                .first()
            )

            if program:
                programs.append({
                    "id": program.id,
                    "name": program.name,
                    "code": program.code
                })

        result.append({
            "id": course.id,
            "code": course.code,
            "name": course.name,
            "credit_hours": course.credit_hours,
            "programs": programs
        })

    return result


# =========================================================
# GET ONE COURSE
# =========================================================

@router.get("/{course_id}")
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):

    course = (
        db.query(Course)
        .filter(
            Course.id == course_id
        )
        .first()
    )

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    relationships = (
        db.query(ProgramCourse)
        .filter(
            ProgramCourse.course_id == course.id
        )
        .all()
    )

    programs = []

    for relationship in relationships:

        program = (
            db.query(Program)
            .filter(
                Program.id == relationship.program_id
            )
            .first()
        )

        if program:
            programs.append({
                "id": program.id,
                "name": program.name,
                "code": program.code
            })

    return {
        "id": course.id,
        "code": course.code,
        "name": course.name,
        "credit_hours": course.credit_hours,
        "programs": programs
    }


# =========================================================
# CREATE COURSE
# =========================================================

@router.post("/")
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Check duplicate course code
    # -----------------------------------------------------

    existing_course = (
        db.query(Course)
        .filter(
            Course.code == course.code
        )
        .first()
    )

    if existing_course:
        raise HTTPException(
            status_code=400,
            detail="Course code already exists"
        )

    # -----------------------------------------------------
    # Check credit hours
    # -----------------------------------------------------

    if course.credit_hours <= 0:
        raise HTTPException(
            status_code=400,
            detail="Credit hours must be greater than 0"
        )

    # -----------------------------------------------------
    # Create course
    # -----------------------------------------------------

    new_course = Course(
        code=course.code,
        name=course.name,
        credit_hours=course.credit_hours
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return {
        "id": new_course.id,
        "code": new_course.code,
        "name": new_course.name,
        "credit_hours": new_course.credit_hours,
        "programs": []
    }


# =========================================================
# UPDATE COURSE
# =========================================================

@router.put("/{course_id}")
def update_course(
    course_id: int,
    course: CourseCreate,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Check if course exists
    # -----------------------------------------------------

    existing_course = (
        db.query(Course)
        .filter(
            Course.id == course_id
        )
        .first()
    )

    if not existing_course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # -----------------------------------------------------
    # Check credit hours
    # -----------------------------------------------------

    if course.credit_hours <= 0:
        raise HTTPException(
            status_code=400,
            detail="Credit hours must be greater than 0"
        )

    # -----------------------------------------------------
    # Check duplicate course code
    # -----------------------------------------------------

    duplicate_course = (
        db.query(Course)
        .filter(
            Course.code == course.code,
            Course.id != course_id
        )
        .first()
    )

    if duplicate_course:
        raise HTTPException(
            status_code=400,
            detail="Course code already exists"
        )

    # -----------------------------------------------------
    # Update course
    # -----------------------------------------------------

    existing_course.code = course.code
    existing_course.name = course.name
    existing_course.credit_hours = course.credit_hours

    db.commit()
    db.refresh(existing_course)

    return {
        "id": existing_course.id,
        "code": existing_course.code,
        "name": existing_course.name,
        "credit_hours": existing_course.credit_hours
    }


# =========================================================
# CONNECT COURSE TO PROGRAM
# =========================================================

@router.post("/{course_id}/programs")
def add_course_to_program(
    course_id: int,
    relationship: ProgramCourseCreate,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Check course
    # -----------------------------------------------------

    course = (
        db.query(Course)
        .filter(
            Course.id == course_id
        )
        .first()
    )

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # -----------------------------------------------------
    # Check program
    # -----------------------------------------------------

    program = (
        db.query(Program)
        .filter(
            Program.id == relationship.program_id
        )
        .first()
    )

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    # -----------------------------------------------------
    # Check duplicate relationship
    # -----------------------------------------------------

    existing_relationship = (
        db.query(ProgramCourse)
        .filter(
            ProgramCourse.course_id == course_id,
            ProgramCourse.program_id == relationship.program_id
        )
        .first()
    )

    if existing_relationship:
        raise HTTPException(
            status_code=400,
            detail="Course is already connected to this program"
        )

    # -----------------------------------------------------
    # Create relationship
    # -----------------------------------------------------

    new_relationship = ProgramCourse(
        course_id=course_id,
        program_id=relationship.program_id
    )

    db.add(new_relationship)
    db.commit()
    db.refresh(new_relationship)

    return {
        "message": "Course connected to program successfully",
        "course_id": course_id,
        "program_id": relationship.program_id
    }


# =========================================================
# REMOVE COURSE FROM PROGRAM
# =========================================================

@router.delete("/{course_id}/programs/{program_id}")
def remove_course_from_program(
    course_id: int,
    program_id: int,
    db: Session = Depends(get_db)
):

    relationship = (
        db.query(ProgramCourse)
        .filter(
            ProgramCourse.course_id == course_id,
            ProgramCourse.program_id == program_id
        )
        .first()
    )

    if not relationship:
        raise HTTPException(
            status_code=404,
            detail="Course-program relationship not found"
        )

    db.delete(relationship)
    db.commit()

    return {
        "message": "Course removed from program successfully",
        "course_id": course_id,
        "program_id": program_id
    }
