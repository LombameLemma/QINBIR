from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.lecturer_availability import LecturerAvailability
from app.models.lecturer import Lecturer
from app.models.time_slot import TimeSlot


router = APIRouter(
    prefix="/lecturer-availability",
    tags=["Lecturer Availability"]
)


class LecturerAvailabilityCreate(BaseModel):
    lecturer_id: int
    time_slot_id: int
    is_available: bool


@router.get("/")
def get_availability(db: Session = Depends(get_db)):
    return db.query(LecturerAvailability).all()


@router.post("/")
def create_availability(
    availability: LecturerAvailabilityCreate,
    db: Session = Depends(get_db)
):
    lecturer = (
        db.query(Lecturer)
        .filter(Lecturer.id == availability.lecturer_id)
        .first()
    )

    if not lecturer:
        raise HTTPException(
            status_code=404,
            detail="Lecturer not found"
        )

    slot = (
        db.query(TimeSlot)
        .filter(TimeSlot.id == availability.time_slot_id)
        .first()
    )

    if not slot:
        raise HTTPException(
            status_code=404,
            detail="Time slot not found"
        )

    new_availability = LecturerAvailability(
        lecturer_id=availability.lecturer_id,
        time_slot_id=availability.time_slot_id,
        is_available=availability.is_available
    )

    db.add(new_availability)
    db.commit()
    db.refresh(new_availability)

    return new_availability