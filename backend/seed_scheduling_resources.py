import sqlite3
from datetime import time

DB_PATH = "qinbir.db"


# ============================================================
# TIME SLOTS
# ============================================================

TIME_SLOTS = []

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
]

# Two-hour teaching periods
long_periods = [
    ("08:00", "10:00"),
    ("10:00", "12:00"),
    ("13:00", "15:00"),
]

# One-hour periods used for short sessions
short_periods = [
    ("08:00", "09:00"),
    ("09:00", "10:00"),
    ("10:00", "11:00"),
    ("11:00", "12:00"),
    ("13:00", "14:00"),
    ("14:00", "15:00"),
]


for day in days:

    for start, end in long_periods:
        TIME_SLOTS.append(
            (day, start, end)
        )

    for start, end in short_periods:
        TIME_SLOTS.append(
            (day, start, end)
        )


# ============================================================
# ROOMS
# ============================================================

ROOMS = [
    ("Room 101", "Main Building", 30, "CLASSROOM"),
    ("Room 102", "Main Building", 30, "CLASSROOM"),
    ("Room 103", "Main Building", 35, "CLASSROOM"),
    ("Room 104", "Main Building", 35, "CLASSROOM"),
    ("Room 105", "Main Building", 40, "CLASSROOM"),

    ("Room 201", "Main Building", 40, "CLASSROOM"),
    ("Room 202", "Main Building", 45, "CLASSROOM"),
    ("Room 203", "Main Building", 50, "CLASSROOM"),
    ("Room 204", "Main Building", 50, "CLASSROOM"),
    ("Room 205", "Main Building", 55, "CLASSROOM"),

    ("Room 301", "Science Building", 60, "CLASSROOM"),
    ("Room 302", "Science Building", 60, "CLASSROOM"),
    ("Room 303", "Science Building", 70, "CLASSROOM"),
    ("Room 304", "Science Building", 80, "CLASSROOM"),

    ("Lecture Hall 1", "Main Building", 100, "LECTURE_HALL"),
    ("Lecture Hall 2", "Main Building", 120, "LECTURE_HALL"),

    ("Lab 1", "Technology Building", 30, "LAB"),
    ("Lab 2", "Technology Building", 30, "LAB"),
    ("Lab 3", "Technology Building", 35, "LAB"),
    ("Lab 4", "Technology Building", 40, "LAB"),
]


def parse_time(value):
    hour, minute = map(int, value.split(":"))
    return time(hour, minute)


def main():

    print("=" * 75)
    print("QINBIR SCHEDULING RESOURCE SEED")
    print("=" * 75)

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON")

    # ========================================================
    # BACKUP CURRENT RESOURCE DATA
    # ========================================================

    print()
    print("Current resources:")

    old_rooms = db.execute(
        "SELECT COUNT(*) FROM rooms"
    ).fetchone()[0]

    old_slots = db.execute(
        "SELECT COUNT(*) FROM time_slots"
    ).fetchone()[0]

    old_availability = db.execute(
        "SELECT COUNT(*) FROM lecturer_availability"
    ).fetchone()[0]

    print(f"  Rooms:          {old_rooms}")
    print(f"  Time slots:     {old_slots}")
    print(f"  Availability:   {old_availability}")

    # ========================================================
    # REMOVE OLD AVAILABILITY
    # ========================================================

    print()
    print("Resetting lecturer availability...")

    db.execute(
        "DELETE FROM lecturer_availability"
    )

    # ========================================================
    # REMOVE OLD TIME SLOTS
    #
    # Schedule entries may reference them, so remove old
    # schedule data first.
    # ========================================================

    print("Resetting old schedule entries...")

    db.execute(
        "DELETE FROM schedule_entries"
    )

    db.execute(
        "DELETE FROM schedules"
    )

    print("Resetting old time slots...")

    db.execute(
        "DELETE FROM time_slots"
    )

    # ========================================================
    # INSERT TIME SLOTS
    # ========================================================

    print()
    print("Creating time slots...")

    slot_ids = []

    for day, start, end in TIME_SLOTS:

        cursor = db.execute(
            """
            INSERT INTO time_slots
            (
                day,
                start_time,
                end_time
            )
            VALUES (?, ?, ?)
            """,
            (
                day,
                parse_time(start).isoformat(),
                parse_time(end).isoformat(),
            )
        )

        slot_ids.append(cursor.lastrowid)

    # ========================================================
    # RESET ROOMS
    # ========================================================

    print("Resetting old rooms...")

    db.execute(
        "DELETE FROM rooms"
    )

    # ========================================================
    # INSERT ROOMS
    # ========================================================

    print("Creating rooms...")

    for name, building, capacity, room_type in ROOMS:

        db.execute(
            """
            INSERT INTO rooms
            (
                name,
                building,
                capacity,
                room_type
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                building,
                capacity,
                room_type,
            )
        )

    # ========================================================
    # LECTURER AVAILABILITY
    # ========================================================

    lecturers = db.execute(
        """
        SELECT id, name
        FROM lecturers
        ORDER BY id
        """
    ).fetchall()

    print()
    print(
        f"Creating availability for {len(lecturers)} lecturers..."
    )

    availability_count = 0

    for lecturer_id, lecturer_name in lecturers:

        for slot_id in slot_ids:

            db.execute(
                """
                INSERT INTO lecturer_availability
                (
                    lecturer_id,
                    time_slot_id,
                    is_available
                )
                VALUES (?, ?, ?)
                """,
                (
                    lecturer_id,
                    slot_id,
                    1,
                )
            )

            availability_count += 1

    db.commit()

    # ========================================================
    # VERIFICATION
    # ========================================================

    room_count = db.execute(
        "SELECT COUNT(*) FROM rooms"
    ).fetchone()[0]

    slot_count = db.execute(
        "SELECT COUNT(*) FROM time_slots"
    ).fetchone()[0]

    availability_count_db = db.execute(
        "SELECT COUNT(*) FROM lecturer_availability"
    ).fetchone()[0]

    lecturer_count = db.execute(
        "SELECT COUNT(*) FROM lecturers"
    ).fetchone()[0]

    print()
    print("=" * 75)
    print("RESOURCE SEED COMPLETE")
    print("=" * 75)

    print(f"Rooms:                    {room_count}")
    print(f"Time slots:               {slot_count}")
    print(f"Lecturers:                {lecturer_count}")
    print(f"Availability records:     {availability_count_db}")

    print()
    print("EXPECTED AVAILABILITY:")
    print(
        f"{lecturer_count} lecturers × "
        f"{slot_count} time slots = "
        f"{lecturer_count * slot_count}"
    )

    # ========================================================
    # ROOMS
    # ========================================================

    print()
    print("ROOMS")
    print("-" * 75)

    rows = db.execute(
        """
        SELECT id, name, building, capacity, room_type
        FROM rooms
        ORDER BY id
        """
    ).fetchall()

    for row in rows:
        print(row)

    # ========================================================
    # TIME SLOTS
    # ========================================================

    print()
    print("TIME SLOTS")
    print("-" * 75)

    rows = db.execute(
        """
        SELECT id, day, start_time, end_time
        FROM time_slots
        ORDER BY
            CASE day
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
                ELSE 6
            END,
            start_time,
            end_time
        """
    ).fetchall()

    for row in rows:
        print(row)

    db.close()

    print()
    print("Database connection closed.")
    print("QINBIR scheduling resources are ready.")


if __name__ == "__main__":
    main()