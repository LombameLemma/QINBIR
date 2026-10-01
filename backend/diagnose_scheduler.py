import sqlite3
from pathlib import Path
from collections import defaultdict


# ============================================================
# DATABASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "qinbir.db"


def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


# ============================================================
# TIME HELPERS
# ============================================================

def time_to_minutes(value):
    if value is None:
        return 0

    value = str(value)
    hours, minutes, *_ = value.split(":")

    return int(hours) * 60 + int(minutes)


def slot_duration(slot):
    return (
        time_to_minutes(slot["end_time"])
        - time_to_minutes(slot["start_time"])
    )


# ============================================================
# MAIN DIAGNOSTIC
# ============================================================

def main():

    db = get_db()

    print()
    print("=" * 70)
    print("QINBIR SCHEDULER FEASIBILITY DIAGNOSTIC")
    print("=" * 70)

    # --------------------------------------------------------
    # BASIC COUNTS
    # --------------------------------------------------------

    requirements = db.execute("""
        SELECT
            cr.id,
            cr.course_id,
            cr.student_section_id,
            cr.lecturer_id,
            cr.sessions_per_week,
            cr.long_session_hours,
            cr.short_session_hours,
            c.code AS course_code,
            c.name AS course_name,
            c.credit_hours,
            ss.name AS section_name,
            ss.student_count,
            l.name AS lecturer_name
        FROM course_requirements cr
        JOIN courses c
            ON c.id = cr.course_id
        JOIN student_sections ss
            ON ss.id = cr.student_section_id
        JOIN lecturers l
            ON l.id = cr.lecturer_id
        ORDER BY cr.id
    """).fetchall()

    lecturers = db.execute("""
        SELECT id, name
        FROM lecturers
        ORDER BY id
    """).fetchall()

    sections = db.execute("""
        SELECT id, name, student_count
        FROM student_sections
        ORDER BY id
    """).fetchall()

    slots = db.execute("""
        SELECT
            id,
            day,
            start_time,
            end_time
        FROM time_slots
        ORDER BY id
    """).fetchall()

    availability = db.execute("""
        SELECT
            lecturer_id,
            time_slot_id,
            is_available
        FROM lecturer_availability
    """).fetchall()

    db.close()

    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    print()
    print("BASIC DATA")
    print("-" * 70)

    print(f"Requirements:        {len(requirements)}")
    print(f"Lecturers:           {len(lecturers)}")
    print(f"Sections:            {len(sections)}")
    print(f"Time slots:          {len(slots)}")

    # ========================================================
    # SLOT GROUPS
    # ========================================================

    long_slots = [
        slot
        for slot in slots
        if slot_duration(slot) == 120
    ]

    short_slots = [
        slot
        for slot in slots
        if slot_duration(slot) == 60
    ]

    print()
    print("TIME SLOT CAPACITY")
    print("-" * 70)

    print(f"2-hour slots:        {len(long_slots)}")
    print(f"1-hour slots:        {len(short_slots)}")

    # ========================================================
    # REQUIREMENT SESSION DEMAND
    # ========================================================

    demand_by_lecturer = defaultdict(lambda: {
        "long": 0,
        "short": 0,
        "requirements": 0,
        "courses": []
    })

    demand_by_section = defaultdict(lambda: {
        "long": 0,
        "short": 0,
        "requirements": 0,
        "courses": []
    })

    for req in requirements:

        credit = int(req["credit_hours"])

        if credit == 2:
            long_sessions = 1
            short_sessions = 0

        elif credit == 3:
            long_sessions = 1
            short_sessions = 1

        elif credit == 4:
            long_sessions = 2
            short_sessions = 0

        else:
            continue

        lecturer_id = req["lecturer_id"]
        section_id = req["student_section_id"]

        demand_by_lecturer[lecturer_id]["long"] += long_sessions
        demand_by_lecturer[lecturer_id]["short"] += short_sessions
        demand_by_lecturer[lecturer_id]["requirements"] += 1
        demand_by_lecturer[lecturer_id]["courses"].append(
            req["course_code"]
        )

        demand_by_section[section_id]["long"] += long_sessions
        demand_by_section[section_id]["short"] += short_sessions
        demand_by_section[section_id]["requirements"] += 1
        demand_by_section[section_id]["courses"].append(
            req["course_code"]
        )

    # ========================================================
    # AVAILABILITY
    # ========================================================

    available = defaultdict(set)

    for row in availability:

        if bool(row["is_available"]):

            available[
                row["lecturer_id"]
            ].add(row["time_slot_id"])

    # ========================================================
    # LECTURER DIAGNOSTIC
    # ========================================================

    lecturer_map = {
        row["id"]: row["name"]
        for row in lecturers
    }

    print()
    print("=" * 70)
    print("LECTURER FEASIBILITY")
    print("=" * 70)

    lecturer_problems = []

    for lecturer_id, demand in demand_by_lecturer.items():

        available_long = sum(
            1
            for slot in long_slots
            if slot["id"] in available[lecturer_id]
        )

        available_short = sum(
            1
            for slot in short_slots
            if slot["id"] in available[lecturer_id]
        )

        required_long = demand["long"]
        required_short = demand["short"]

        problem = (
            available_long < required_long
            or available_short < required_short
        )

        if problem:

            lecturer_problems.append({
                "id": lecturer_id,
                "name": lecturer_map.get(
                    lecturer_id,
                    f"Lecturer {lecturer_id}"
                ),
                "required_long": required_long,
                "available_long": available_long,
                "required_short": required_short,
                "available_short": available_short,
                "requirements": demand["requirements"],
                "courses": demand["courses"]
            })

    if not lecturer_problems:

        print("No obvious lecturer-capacity problems found.")

    else:

        print(
            f"Found {len(lecturer_problems)} lecturer(s) "
            "with insufficient raw availability."
        )

        print()

        for item in lecturer_problems[:30]:

            print(
                f"Lecturer {item['id']} - {item['name']}"
            )

            print(
                f"  Requirements:     {item['requirements']}"
            )

            print(
                f"  Required 2h:      {item['required_long']}"
            )

            print(
                f"  Available 2h:     {item['available_long']}"
            )

            print(
                f"  Required 1h:      {item['required_short']}"
            )

            print(
                f"  Available 1h:     {item['available_short']}"
            )

            print(
                f"  Courses:          "
                f"{', '.join(item['courses'][:10])}"
            )

            print()

    # ========================================================
    # SECTION DIAGNOSTIC
    # ========================================================

    section_map = {
        row["id"]: row["name"]
        for row in sections
    }

    print()
    print("=" * 70)
    print("SECTION FEASIBILITY")
    print("=" * 70)

    section_problems = []

    for section_id, demand in demand_by_section.items():

        required_sessions = (
            demand["long"] +
            demand["short"]
        )

        # A section can use at most one class at a time.
        # There are 45 available slots in total.
        if required_sessions > len(slots):

            section_problems.append({
                "id": section_id,
                "name": section_map.get(
                    section_id,
                    f"Section {section_id}"
                ),
                "required": required_sessions
            })

    if not section_problems:

        print("No section exceeds the total number of time slots.")

    else:

        print(
            f"Found {len(section_problems)} section(s) "
            "with more sessions than available slots."
        )

        for item in section_problems:

            print(
                f"Section {item['id']} - {item['name']}: "
                f"{item['required']} sessions"
            )

    # ========================================================
    # GLOBAL DEMAND
    # ========================================================

    total_long = sum(
        item["long"]
        for item in demand_by_lecturer.values()
    )

    total_short = sum(
        item["short"]
        for item in demand_by_lecturer.values()
    )

    print()
    print("=" * 70)
    print("TOTAL DEMAND")
    print("=" * 70)

    print(f"2-hour sessions required: {total_long}")
    print(f"1-hour sessions required: {total_short}")
    print(
        f"Total sessions required:  {total_long + total_short}"
    )

    # ========================================================
    # LECTURER CAPACITY
    # ========================================================

    total_available_long = sum(
        sum(
            1
            for slot in long_slots
            if slot["id"] in available[lecturer["id"]]
        )
        for lecturer in lecturers
    )

    total_available_short = sum(
        sum(
            1
            for slot in short_slots
            if slot["id"] in available[lecturer["id"]]
        )
        for lecturer in lecturers
    )

    print()
    print("=" * 70)
    print("LECTURER RAW CAPACITY")
    print("=" * 70)

    print(
        f"Available 2-hour lecturer slots: "
        f"{total_available_long}"
    )

    print(
        f"Required 2-hour sessions:         "
        f"{total_long}"
    )

    print(
        f"Available 1-hour lecturer slots: "
        f"{total_available_short}"
    )

    print(
        f"Required 1-hour sessions:         "
        f"{total_short}"
    )

    # ========================================================
    # FINAL
    # ========================================================

    print()
    print("=" * 70)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()