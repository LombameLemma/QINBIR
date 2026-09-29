from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.lecturer import Lecturer
from app.models.department import Department
from app.models.user import User


router = APIRouter(
    prefix="/lecturers",
    tags=["Lecturers"]
)


class LecturerCreate(BaseModel):
    user_id: int
    department_id: int
    employee_id: str
    name: str


@router.get("/")
def get_lecturers(db: Session = Depends(get_db)):
    lecturers = db.query(Lecturer).all()

    return lecturers


@router.post("/")
def create_lecturer(
    lecturer: LecturerCreate,
    db: Session = Depends(get_db)
):
    # Check that the user exists
    user = (
        db.query(User)
        .filter(User.id == lecturer.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check that the department exists
    department = (
        db.query(Department)
        .filter(Department.id == lecturer.department_id)
        .first()
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    # Check duplicate employee ID
    existing_lecturer = (
        db.query(Lecturer)
        .filter(Lecturer.employee_id == lecturer.employee_id)
        .first()
    )

    if existing_lecturer:
        raise HTTPException(
            status_code=400,
            detail="Employee ID already exists"
        )

    new_lecturer = Lecturer(
        user_id=lecturer.user_id,
        department_id=lecturer.department_id,
        employee_id=lecturer.employee_id,
        name=lecturer.name
    )

    db.add(new_lecturer)
    db.commit()
    db.refresh(new_lecturer)

    return new_lecturer