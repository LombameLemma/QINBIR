
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.program import Program
from app.models.department import Department


router = APIRouter(
    prefix="/programs",
    tags=["Programs"]
)


# Request model for creating a program
class ProgramCreate(BaseModel):
    name: str = Field(min_length=1)
    code: str = Field(min_length=1)
    department_id: int = Field(gt=0)


# Request model for updating a program
class ProgramUpdate(BaseModel):
    name: str = Field(min_length=1)
    code: str = Field(min_length=1)
    department_id: int = Field(gt=0)


# READ: Get all programs
@router.get("/")
def get_programs(db: Session = Depends(get_db)):
    return db.query(Program).all()


# CREATE: Add a program
@router.post("/")
def create_program(
    program: ProgramCreate,
    db: Session = Depends(get_db)
):
    name = program.name.strip()
    code = program.code.strip().upper()

    if not name or not code:
        raise HTTPException(
            status_code=422,
            detail="Program name and code cannot be empty."
        )

    department = (
        db.query(Department)
        .filter(Department.id == program.department_id)
        .first()
    )

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found."
        )

    existing_program = (
        db.query(Program)
        .filter(Program.code == code)
        .first()
    )

    if existing_program:
        raise HTTPException(
            status_code=409,
            detail="Program code already exists."
        )

    new_program = Program(
        name=name,
        code=code,
        department_id=program.department_id
    )

    try:
        db.add(new_program)
        db.commit()
        db.refresh(new_program)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not create the program. Check that its code is unique and its department exists."
        )

    return new_program


# UPDATE: Edit an existing program
@router.put("/{program_id}")
def update_program(
    program_id: int,
    program: ProgramUpdate,
    db: Session = Depends(get_db)
):
    existing_program = (
        db.query(Program)
        .filter(Program.id == program_id)
        .first()
    )

    if existing_program is None:
        raise HTTPException(
            status_code=404,
            detail="Program not found."
        )

    name = program.name.strip()
    code = program.code.strip().upper()

    if not name or not code:
        raise HTTPException(
            status_code=422,
            detail="Program name and code cannot be empty."
        )

    department = (
        db.query(Department)
        .filter(Department.id == program.department_id)
        .first()
    )

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found."
        )

    duplicate_code = (
        db.query(Program)
        .filter(
            Program.code == code,
            Program.id != program_id
        )
        .first()
    )

    if duplicate_code:
        raise HTTPException(
            status_code=409,
            detail="Another program already uses this code."
        )

    existing_program.name = name
    existing_program.code = code
    existing_program.department_id = program.department_id

    try:
        db.commit()
        db.refresh(existing_program)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not update the program. Check its code and department."
        )

    return existing_program


# DELETE: Remove an existing program
@router.delete("/{program_id}")
def delete_program(
    program_id: int,
    db: Session = Depends(get_db)
):
    existing_program = (
        db.query(Program)
        .filter(Program.id == program_id)
        .first()
    )

    if existing_program is None:
        raise HTTPException(
            status_code=404,
            detail="Program not found."
        )

    try:
        db.delete(existing_program)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=(
                "This program cannot be deleted because other records "
                "may reference it. Reassign or remove those records first."
            )
        )

    return {
        "message": "Program deleted successfully.",
        "id": program_id
    }
