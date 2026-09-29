from datetime import time

from app.database import SessionLocal

from app.models.lecturer import Lecturer
from app.models.time_slot import TimeSlot
from app.models.lecturer_availability import LecturerAvailability


db = SessionLocal()

try:
    lecturer = db.query(Lecturer).filter(
        Lecturer.employee_id == "LEC001"
    ).first()

    if not lecturer:
        print("Dr. Abebe was not found.")
        raise SystemExit

    # Find the original test restriction: Monday 08:00–10:00
    monday_slot = db.query(TimeSlot).filter(
        TimeSlot.day == "Monday",
        TimeSlot.start_time == time(8, 0),
        TimeSlot.end_time == time(10, 0),
    ).first()

    if not monday_slot:
        print("Monday 08:00–10:00 slot was not found.")
        raise SystemExit

    # Make all recorded slots available for Dr. Abebe
    db.query(LecturerAvailability).filter(
        LecturerAvailability.lecturer_id == lecturer.id
    ).update(
        {LecturerAvailability.is_available: True},
        synchronize_session=False,
    )

    # Reinstate the original Monday morning restriction
    monday_availability = db.query(
        LecturerAvailability
    ).filter(
        LecturerAvailability.lecturer_id == lecturer.id,
        LecturerAvailability.time_slot_id == monday_slot.id,
    ).first()

    if monday_availability:
        monday_availability.is_available = False
    else:
        db.add(
            LecturerAvailability(
                lecturer_id=lecturer.id,
                time_slot_id=monday_slot.id,
                is_available=False,
            )
        )

    db.commit()

    print()
    print("Availability restored for Dr. Abebe.")
    print("Monday 08:00–10:00: UNAVAILABLE")
    print("Other recorded slots: AVAILABLE")

except Exception as e:
    db.rollback()
    print("Error restoring availability:")
    print(e)

finally:
    db.close()