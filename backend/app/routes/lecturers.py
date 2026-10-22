
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.lecturer import Lecturer
from app.models.department import Department
from app.models.user import User


router = APIRouter(
    prefix="/lecturers",
    tags=["Lecturers"]
)


class LecturerCreate(BaseModel):
    user_id: int = Field(gt=0)
    department_id: int = Field(gt=0)
    employee_id: str = Field(min_length=1)
    name: str = Field(min_length=1)


def validate_references(lecturer, db: Session):
    user = db.query(User).filter(
        User.id == lecturer.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    department = db.query(Department).filter(
        Department.id == lecturer.department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )


# READ
@router.get("/")
def get_lecturers(db: Session = Depends(get_db)):
    return db.query(Lecturer).all()


# CREATE
@router.post("/")
def create_lecturer(
    lecturer: LecturerCreate,
    db: Session = Depends(get_db)
):
    employee_id = lecturer.employee_id.strip()
    name = lecturer.name.strip()

    if not employee_id or not name:
        raise HTTPException(
            status_code=422,
            detail="Employee ID and name cannot be empty"
        )

    validate_references(lecturer, db)

    duplicate = db.query(Lecturer).filter(
        Lecturer.employee_id == employee_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="Employee ID already exists"
        )

    new_lecturer = Lecturer(
        user_id=lecturer.user_id,
        department_id=lecturer.department_id,
        employee_id=employee_id,
        name=name
    )

    try:
        db.add(new_lecturer)
        db.commit()
        db.refresh(new_lecturer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not create lecturer because of a data conflict"
        )

    return new_lecturer


# UPDATE
@router.put("/{lecturer_id}")
def update_lecturer(
    lecturer_id: int,
    lecturer: LecturerCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Lecturer).filter(
        Lecturer.id == lecturer_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Lecturer not found"
        )

    employee_id = lecturer.employee_id.strip()
    name = lecturer.name.strip()

    if not employee_id or not name:
        raise HTTPException(
            status_code=422,
            detail="Employee ID and name cannot be empty"
        )

    validate_references(lecturer, db)

    duplicate = db.query(Lecturer).filter(
        Lecturer.employee_id == employee_id,
        Lecturer.id != lecturer_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="Employee ID already exists"
        )

    existing.user_id = lecturer.user_id
    existing.department_id = lecturer.department_id
    existing.employee_id = employee_id
    existing.name = name

    try:
        db.commit()
        db.refresh(existing)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not update lecturer because of a data conflict"
        )

    return existing


# DELETE
@router.delete("/{lecturer_id}")
def delete_lecturer(
    lecturer_id: int,
    db: Session = Depends(get_db)
):
    existing = db.query(Lecturer).filter(
        Lecturer.id == lecturer_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Lecturer not found"
        )

    try:
        db.delete(existing)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=(
                "This lecturer cannot be deleted because other records "
                "may reference them. Reassign or remove those records first."
            )
        )

    return {
        "message": "Lecturer deleted successfully",
        "id": lecturer_id
    }
