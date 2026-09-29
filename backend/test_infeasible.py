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

    # Find Monday, Tuesday and Wednesday morning slots
    target_times = [
        ("Monday", time(8, 0), time(10, 0)),
        ("Tuesday", time(8, 0), time(10, 0)),
        ("Wednesday", time(8, 0), time(10, 0)),
        ("Monday", time(10, 0), time(12, 0)),
        ("Tuesday", time(10, 0), time(12, 0)),
        ("Wednesday", time(10, 0), time(12, 0)),
        ("Monday", time(13, 0), time(15, 0)),
        ("Tuesday", time(13, 0), time(15, 0)),
        ("Wednesday", time(13, 0), time(15, 0)),
    ]

    slots = []

    for day, start, end in target_times:

        slot = db.query(TimeSlot).filter(
            TimeSlot.day == day,
            TimeSlot.start_time == start,
            TimeSlot.end_time == end,
        ).first()

        if slot:
            slots.append(slot)

    if not slots:
        print("No matching time slots were found.")
        raise SystemExit

    print()
    print("QINBIR Infeasibility Test")
    print("=========================")
    print(f"Lecturer: {lecturer.name}")
    print()

    # Make every available slot unavailable for Dr. Abebe
    for slot in slots:

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

        print(
            f"Marked unavailable: "
            f"{slot.day} "
            f"{slot.start_time} - "
            f"{slot.end_time}"
        )

    db.commit()

    print()
    print(
        "All selected time slots are now unavailable "
        "for Dr. Abebe."
    )
    print()
    print("Infeasibility test data saved successfully.")

except Exception as e:

    db.rollback()

    print()
    print("Error:")
    print(e)

finally:
    db.close()