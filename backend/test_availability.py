from datetime import time

from app.database import SessionLocal

from app.models.lecturer import Lecturer
from app.models.time_slot import TimeSlot
from app.models.lecturer_availability import LecturerAvailability


db = SessionLocal()

try:

    # Find Dr. Abebe
    lecturer = db.query(Lecturer).filter(
        Lecturer.employee_id == "LEC001"
    ).first()

    if not lecturer:
        print("Dr. Abebe was not found.")
        raise SystemExit

    # Find Monday 08:00 - 10:00
    slot = db.query(TimeSlot).filter(
        TimeSlot.day == "Monday",
        TimeSlot.start_time == time(8, 0),
        TimeSlot.end_time == time(10, 0),
    ).first()

    if not slot:
        print("Monday 08:00-10:00 slot was not found.")
        raise SystemExit

    # Check whether the restriction already exists
    availability = db.query(
        LecturerAvailability
    ).filter(
        LecturerAvailability.lecturer_id == lecturer.id,
        LecturerAvailability.time_slot_id == slot.id,
    ).first()

    if availability:
        availability.is_available = False
    else:
        availability = LecturerAvailability(
            lecturer_id=lecturer.id,
            time_slot_id=slot.id,
            is_available=False,
        )
        db.add(availability)

    db.commit()

    print()
    print("QINBIR Lecturer Availability Test")
    print("==================================")
    print(f"Lecturer: {lecturer.name}")
    print(
        f"Time: {slot.day} "
        f"{slot.start_time} - "
        f"{slot.end_time}"
    )
    print("Availability: UNAVAILABLE")
    print()
    print("Availability restriction saved successfully!")

except Exception as e:

    db.rollback()

    print()
    print("Error:")
    print(e)

finally:
    db.close()