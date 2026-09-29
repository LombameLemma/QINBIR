from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import time

from app.database import get_db
from app.models.time_slot import TimeSlot


router = APIRouter(
    prefix="/time-slots",
    tags=["Time Slots"]
)


class TimeSlotCreate(BaseModel):
    day: str
    start_time: time
    end_time: time


@router.get("/")
def get_time_slots(db: Session = Depends(get_db)):
    return db.query(TimeSlot).all()


@router.post("/")
def create_time_slot(
    slot: TimeSlotCreate,
    db: Session = Depends(get_db)
):
    new_slot = TimeSlot(
        day=slot.day,
        start_time=slot.start_time,
        end_time=slot.end_time
    )

    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)

    return new_slot