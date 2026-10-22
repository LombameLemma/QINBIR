
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.room import Room


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


# Request model for creating a room
class RoomCreate(BaseModel):
    name: str
    building: str
    capacity: int = Field(gt=0)
    room_type: str


# Request model for updating a room
class RoomUpdate(BaseModel):
    name: str
    building: str
    capacity: int = Field(gt=0)
    room_type: str


# READ: Get all rooms
@router.get("/")
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


# CREATE: Add a new room
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


# UPDATE: Edit an existing room
@router.put("/{room_id}")
def update_room(
    room_id: int,
    room: RoomUpdate,
    db: Session = Depends(get_db)
):
    existing_room = (
        db.query(Room)
        .filter(Room.id == room_id)
        .first()
    )

    if existing_room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found."
        )

    existing_room.name = room.name
    existing_room.building = room.building
    existing_room.capacity = room.capacity
    existing_room.room_type = room.room_type

    db.commit()
    db.refresh(existing_room)

    return existing_room


# DELETE: Remove an existing room
@router.delete("/{room_id}")
def delete_room(
    room_id: int,
    db: Session = Depends(get_db)
):
    existing_room = (
        db.query(Room)
        .filter(Room.id == room_id)
        .first()
    )

    if existing_room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found."
        )

    try:
        db.delete(existing_room)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=(
                "This room cannot be deleted because it is "
                "referenced by existing records. "
                "Remove or reassign those references first."
            )
        )

    return {
        "message": "Room deleted successfully.",
        "id": room_id
    }
