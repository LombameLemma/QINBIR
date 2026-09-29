from datetime import time

from app.database import SessionLocal
from app.models.time_slot import TimeSlot


db = SessionLocal()

try:

    slots_to_add = [
        # Monday
        ("Monday", time(8, 0), time(9, 0)),
        ("Monday", time(9, 0), time(10, 0)),
        ("Monday", time(10, 0), time(11, 0)),
        ("Monday", time(11, 0), time(12, 0)),
        ("Monday", time(13, 0), time(14, 0)),
        ("Monday", time(14, 0), time(15, 0)),

        # Tuesday
        ("Tuesday", time(8, 0), time(9, 0)),
        ("Tuesday", time(9, 0), time(10, 0)),
        ("Tuesday", time(10, 0), time(11, 0)),
        ("Tuesday", time(11, 0), time(12, 0)),
        ("Tuesday", time(13, 0), time(14, 0)),
        ("Tuesday", time(14, 0), time(15, 0)),

        # Wednesday
        ("Wednesday", time(8, 0), time(9, 0)),
        ("Wednesday", time(9, 0), time(10, 0)),
        ("Wednesday", time(10, 0), time(11, 0)),
        ("Wednesday", time(11, 0), time(12, 0)),
        ("Wednesday", time(13, 0), time(14, 0)),
        ("Wednesday", time(14, 0), time(15, 0)),
    ]

    added = 0

    for day, start, end in slots_to_add:

        existing = db.query(TimeSlot).filter(
            TimeSlot.day == day,
            TimeSlot.start_time == start,
            TimeSlot.end_time == end,
        ).first()

        if not existing:

            db.add(
                TimeSlot(
                    day=day,
                    start_time=start,
                    end_time=end,
                )
            )

            added += 1

    db.commit()

    print()
    print("QINBIR Time Slot Update")
    print("=======================")
    print(f"New 1-hour slots added: {added}")
    print("Time slot update completed successfully.")

except Exception as e:

    db.rollback()

    print()
    print("Error:")
    print(e)

finally:
    db.close()