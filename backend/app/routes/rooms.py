from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.room import Room


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


class RoomCreate(BaseModel):
    name: str
    building: str
    capacity: int
    room_type: str


@router.get("/")
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


@router.post("/")
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db)
):
    new_room = Room(
        name=room.name,
        building=room.building,
        capacity=room.capacity,
        room_type=room.room_type
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return new_room