from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.student_section import StudentSection
from app.models.program import Program


router = APIRouter(
    prefix="/student-sections",
    tags=["Student Sections"]
)


class StudentSectionCreate(BaseModel):
    name: str
    program_id: int
    year: int
    semester: int
    student_count: int


@router.get("/")
def get_student_sections(db: Session = Depends(get_db)):
    return db.query(StudentSection).all()


@router.post("/")
def create_student_section(
    section: StudentSectionCreate,
    db: Session = Depends(get_db)
):
    program = (
        db.query(Program)
        .filter(Program.id == section.program_id)
        .first()
    )

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    new_section = StudentSection(
        name=section.name,
        program_id=section.program_id,
        year=section.year,
        semester=section.semester,
        student_count=section.student_count
    )

    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    return new_section