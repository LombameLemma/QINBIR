
from app.database import SessionLocal
from app.models.schedule_entry import ScheduleEntry
from app.models.time_slot import TimeSlot

SCHEDULE_ID = 1

db = SessionLocal()

try:
    rows = (
        db.query(ScheduleEntry, TimeSlot)
        .join(TimeSlot, ScheduleEntry.time_slot_id == TimeSlot.id)
        .filter(ScheduleEntry.schedule_id == SCHEDULE_ID)
        .all()
    )

    conflicts = []

    for i, (entry_a, slot_a) in enumerate(rows):
        for entry_b, slot_b in rows[i + 1:]:
            if slot_a.day != slot_b.day:
                continue

            overlaps = (
                slot_a.start_time < slot_b.end_time
                and slot_b.start_time < slot_a.end_time
            )

            if not overlaps:
                continue

            if entry_a.lecturer_id == entry_b.lecturer_id:
                conflicts.append(
                    f"LECTURER clash: entries {entry_a.id} and "
                    f"{entry_b.id}, lecturer {entry_a.lecturer_id}"
                )

            if entry_a.room_id == entry_b.room_id:
                conflicts.append(
                    f"ROOM clash: entries {entry_a.id} and "
                    f"{entry_b.id}, room {entry_a.room_id}"
                )

            if entry_a.student_section_id == entry_b.student_section_id:
                conflicts.append(
                    f"SECTION clash: entries {entry_a.id} and "
                    f"{entry_b.id}, section {entry_a.student_section_id}"
                )

    print(f"\nSchedule ID: {SCHEDULE_ID}")
    print(f"Entries checked: {len(rows)}")

    if conflicts:
        print(f"\nCONFLICTS FOUND: {len(conflicts)}")
        for conflict in conflicts:
            print("-", conflict)
    else:
        print("\nPASS: No lecturer, room, or section clashes found.")

finally:
    db.close()
