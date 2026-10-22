
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.department import Department


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


# Request model for creating a department
class DepartmentCreate(BaseModel):
    name: str = Field(min_length=1)
    code: str = Field(min_length=1)


# Request model for updating a department
class DepartmentUpdate(BaseModel):
    name: str = Field(min_length=1)
    code: str = Field(min_length=1)


# READ: Get all departments
@router.get("/")
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()


# CREATE: Add a department
@router.post("/")
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):
    new_department = Department(
        name=department.name.strip(),
        code=department.code.strip().upper()
    )

    if not new_department.name or not new_department.code:
        raise HTTPException(
            status_code=422,
            detail="Department name and code cannot be empty."
        )

    try:
        db.add(new_department)
        db.commit()
        db.refresh(new_department)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A department with this code may already exist, or the data conflicts with existing records."
        )

    return new_department


# UPDATE: Edit an existing department
@router.put("/{department_id}")
def update_department(
    department_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db)
):
    existing_department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )

    if existing_department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found."
        )

    name = department.name.strip()
    code = department.code.strip().upper()

    if not name or not code:
        raise HTTPException(
            status_code=422,
            detail="Department name and code cannot be empty."
        )

    existing_department.name = name
    existing_department.code = code

    try:
        db.commit()
        db.refresh(existing_department)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="The department code may already be in use, or the update conflicts with existing records."
        )

    return existing_department


# DELETE: Remove a department
@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    existing_department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )

    if existing_department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found."
        )

    try:
        db.delete(existing_department)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=(
                "This department cannot be deleted because other records "
                "may reference it. Reassign or remove those records first."
            )
        )

    return {
        "message": "Department deleted successfully.",
        "id": department_id
    }
