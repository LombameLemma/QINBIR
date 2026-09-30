from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.program import Program
from app.models.department import Department


router = APIRouter(
    prefix="/programs",
    tags=["Programs"]
)


class ProgramCreate(BaseModel):
    name: str
    code: str
    department_id: int


@router.get("/")
def get_programs(db: Session = Depends(get_db)):
    return db.query(Program).all()


@router.post("/")
def create_program(
    program: ProgramCreate,
    db: Session = Depends(get_db)
):
    department = (
        db.query(Department)
        .filter(Department.id == program.department_id)
        .first()
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    existing_program = (
        db.query(Program)
        .filter(Program.code == program.code)
        .first()
    )

    if existing_program:
        raise HTTPException(
            status_code=400,
            detail="Program code already exists"
        )

    new_program = Program(
        name=program.name,
        code=program.code,
        department_id=program.department_id
    )

    db.add(new_program)
    db.commit()
    db.refresh(new_program)

    return new_program