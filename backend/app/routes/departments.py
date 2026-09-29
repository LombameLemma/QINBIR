from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.department import Department


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


class DepartmentCreate(BaseModel):
    name: str
    code: str


@router.get("/")
def get_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).all()

    return departments


@router.post("/")
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):
    existing_department = (
        db.query(Department)
        .filter(Department.code == department.code)
        .first()
    )

    if existing_department:
        return {
            "message": "Department code already exists",
            "department": existing_department
        }

    new_department = Department(
        name=department.name,
        code=department.code
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department