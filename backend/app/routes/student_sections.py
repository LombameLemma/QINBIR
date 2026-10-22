
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.student_section import StudentSection
from app.models.program import Program


router = APIRouter(
    prefix="/student-sections",
    tags=["Student Sections"]
)


class StudentSectionCreate(BaseModel):
    name: str = Field(min_length=1)
    program_id: int = Field(gt=0)
    year: int = Field(gt=0)
    semester: int = Field(gt=0)
    student_count: int = Field(ge=0)


def validate_program(program_id: int, db: Session):
    program = db.query(Program).filter(
        Program.id == program_id
    ).first()

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )


# READ
@router.get("/")
def get_student_sections(db: Session = Depends(get_db)):
    return db.query(StudentSection).all()


# CREATE
@router.post("/")
def create_student_section(
    section: StudentSectionCreate,
    db: Session = Depends(get_db)
):
    validate_program(section.program_id, db)

    new_section = StudentSection(
        name=section.name.strip(),
        program_id=section.program_id,
        year=section.year,
        semester=section.semester,
        student_count=section.student_count
    )

    try:
        db.add(new_section)
        db.commit()
        db.refresh(new_section)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not create student section because of a data conflict"
        )

    return new_section


# UPDATE
@router.put("/{section_id}")
def update_student_section(
    section_id: int,
    section: StudentSectionCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(StudentSection).filter(
        StudentSection.id == section_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Student section not found"
        )

    validate_program(section.program_id, db)

    existing.name = section.name.strip()
    existing.program_id = section.program_id
    existing.year = section.year
    existing.semester = section.semester
    existing.student_count = section.student_count

    try:
        db.commit()
        db.refresh(existing)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not update student section because of a data conflict"
        )

    return existing


# DELETE
@router.delete("/{section_id}")
def delete_student_section(
    section_id: int,
    db: Session = Depends(get_db)
):
    existing = db.query(StudentSection).filter(
        StudentSection.id == section_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Student section not found"
        )

    try:
        db.delete(existing)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=(
                "This section cannot be deleted because other records "
                "may reference it. Reassign or remove those records first."
            )
        )

    return {
        "message": "Student section deleted successfully",
        "id": section_id
    }
