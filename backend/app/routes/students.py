
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.student import Student
from app.models.program import Program
from app.models.student_section import StudentSection
from app.security import hash_password, require_role


router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


class StudentCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    student_id: str = Field(min_length=1, max_length=50)
    program_id: int = Field(gt=0)
    section_id: int = Field(gt=0)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_student(
    data: StudentCreate,
    current_user: User = Depends(require_role("ADMIN")),
    db: Session = Depends(get_db),
):
    email = str(data.email).strip().lower()
    student_id = data.student_id.strip()

    if not student_id:
        raise HTTPException(
            status_code=400,
            detail="Student ID cannot be empty.",
        )

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists.",
        )

    existing_student = (
        db.query(Student)
        .filter(Student.student_id == student_id)
        .first()
    )
    if existing_student:
        raise HTTPException(
            status_code=409,
            detail="This student ID already exists.",
        )

    program = db.query(Program).filter(Program.id == data.program_id).first()
    if program is None:
        raise HTTPException(
            status_code=404,
            detail="Program not found.",
        )

    section = (
        db.query(StudentSection)
        .filter(StudentSection.id == data.section_id)
        .first()
    )
    if section is None:
        raise HTTPException(
            status_code=404,
            detail="Student section not found.",
        )

    if section.program_id != program.id:
        raise HTTPException(
            status_code=400,
            detail="The selected section does not belong to the selected program.",
        )

    try:
        user = User(
            full_name=data.full_name.strip(),
            email=email,
            password_hash=hash_password(data.password),
            role="STUDENT",
            is_active=True,
        )
        db.add(user)
        db.flush()

        student = Student(
            user_id=user.id,
            student_id=student_id,
            program_id=program.id,
            section_id=section.id,
        )
        db.add(student)
        db.commit()
        db.refresh(user)
        db.refresh(student)

        return {
            "message": "Student account created successfully.",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role,
            },
            "student": {
                "id": student.id,
                "student_id": student.student_id,
                "program_id": student.program_id,
                "section_id": student.section_id,
            },
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Student creation failed. No changes were saved.",
        )
