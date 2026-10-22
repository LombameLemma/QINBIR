
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.time_slot import TimeSlot


router = APIRouter(
    prefix="/time-slots",
    tags=["Time Slots"]
)


class TimeSlotCreate(BaseModel):
    day: str = Field(min_length=1)
    start_time: str = Field(min_length=1)
    end_time: str = Field(min_length=1)


def validate_times(slot: TimeSlotCreate):
    days = {
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    }

    if slot.day.strip().title() not in days:
        raise HTTPException(
            status_code=422,
            detail="Please provide a valid day of the week"
        )

    if slot.start_time >= slot.end_time:
        raise HTTPException(
            status_code=422,
            detail="End time must be later than start time"
        )


# READ
@router.get("/")
def get_time_slots(db: Session = Depends(get_db)):
    return db.query(TimeSlot).all()


# CREATE
@router.post("/")
def create_time_slot(
    slot: TimeSlotCreate,
    db: Session = Depends(get_db)
):
    validate_times(slot)

    new_slot = TimeSlot(
        day=slot.day.strip().title(),
        start_time=slot.start_time,
        end_time=slot.end_time
    )

    try:
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not create time slot because of a data conflict"
        )

    return new_slot


# UPDATE
@router.put("/{slot_id}")
def update_time_slot(
    slot_id: int,
    slot: TimeSlotCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(TimeSlot).filter(
        TimeSlot.id == slot_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Time slot not found"
        )

    validate_times(slot)

    existing.day = slot.day.strip().title()
    existing.start_time = slot.start_time
    existing.end_time = slot.end_time

    try:
        db.commit()
        db.refresh(existing)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not update time slot because of a data conflict"
        )

    return existing


# DELETE
@router.delete("/{slot_id}")
def delete_time_slot(
    slot_id: int,
    db: Session = Depends(get_db)
):
    existing = db.query(TimeSlot).filter(
        TimeSlot.id == slot_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Time slot not found"
        )

    try:
        db.delete(existing)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=(
                "This time slot cannot be deleted because availability "
                "or other records may reference it."
            )
        )

    return {
        "message": "Time slot deleted successfully",
        "id": slot_id
    }
