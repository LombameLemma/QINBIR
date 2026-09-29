from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.constraint import Constraint


router = APIRouter(
    prefix="/constraints",
    tags=["Constraints"]
)


class ConstraintCreate(BaseModel):
    name: str
    type: str
    description: str | None = None
    is_active: bool = True
    weight: int = 1


@router.get("/")
def get_constraints(db: Session = Depends(get_db)):
    return db.query(Constraint).all()


@router.post("/")
def create_constraint(
    constraint: ConstraintCreate,
    db: Session = Depends(get_db)
):
    new_constraint = Constraint(
        name=constraint.name,
        type=constraint.type,
        description=constraint.description,
        is_active=constraint.is_active,
        weight=constraint.weight
    )

    db.add(new_constraint)
    db.commit()
    db.refresh(new_constraint)

    return new_constraint