from app.database import SessionLocal

from app.models.schedule import Schedule
from app.models.schedule_entry import ScheduleEntry
from app.models.course_requirement import CourseRequirement
from app.models.time_slot import TimeSlot


db = SessionLocal()
passed = True


def pass_test(message):
    print(f"✓ {message}: PASS")


def fail_test(message, details=""):
    global passed

    passed = False

    print(f"✗ {message}: FAIL")

    if details:
        print(f"  {details}")


def slot_duration(slot):
    start_minutes = (
        slot.start_time.hour * 60
        + slot.start_time.minute
    )

    end_minutes = (
        slot.end_time.hour * 60
        + slot.end_time.minute
    )

    return (end_minutes - start_minutes) / 60


try:

    print()
    print("QINBIR Course Session Validation")
    print("================================")

    # ---------------------------------------------------------
    # Find automatic schedule
    # ---------------------------------------------------------

    schedule = (
        db.query(Schedule)
        .filter(
            Schedule.name == "Automatically Generated Schedule",
            Schedule.status == "DRAFT",
        )
        .first()
    )

    if not schedule:

        fail_test(
            "Automatic schedule exists",
            "No automatic draft schedule was found."
        )

        raise SystemExit

    pass_test(
        f"Automatic schedule exists (ID {schedule.id})"
    )

    # ---------------------------------------------------------
    # Load data
    # ---------------------------------------------------------

    requirements = (
        db.query(CourseRequirement)
        .all()
    )

    entries = (
        db.query(ScheduleEntry)
        .filter(
            ScheduleEntry.schedule_id == schedule.id
        )
        .all()
    )

    slots = {
        slot.id: slot
        for slot in db.query(TimeSlot).all()
    }

    entries_by_requirement = {}

    for entry in entries:

        entries_by_requirement.setdefault(
            entry.course_requirement_id,
            []
        ).append(entry)

    # ---------------------------------------------------------
    # Validate each course requirement
    # ---------------------------------------------------------

    for requirement in requirements:

        requirement_entries = entries_by_requirement.get(
            requirement.id,
            []
        )

        print()
        print(
            f"Requirement {requirement.id}"
        )
        print("----------------")

        if len(requirement_entries) != 2:

            fail_test(
                "Exactly 2 sessions",
                (
                    f"Found {len(requirement_entries)} "
                    f"instead of 2."
                )
            )

            continue

        durations = []
        days = []

        for entry in requirement_entries:

            slot = slots.get(entry.time_slot_id)

            if not slot:

                fail_test(
                    "Time slot exists",
                    (
                        f"Entry {entry.id} references "
                        f"missing slot {entry.time_slot_id}."
                    )
                )

                continue

            duration = slot_duration(slot)

            durations.append(duration)
            days.append(slot.day)

            print(
                f"  {slot.day} "
                f"{slot.start_time} - "
                f"{slot.end_time} "
                f"({duration:g} hour)"
            )

        # -----------------------------------------------------
        # Check 2h + 1h
        # -----------------------------------------------------

        durations.sort()

        if durations == [1, 2]:

            pass_test(
                "Course has 2-hour + 1-hour sessions"
            )

        else:

            fail_test(
                "Course has 2-hour + 1-hour sessions",
                f"Found durations: {durations}"
            )

        # -----------------------------------------------------
        # Check different days
        # -----------------------------------------------------

        if len(days) == 2 and days[0] != days[1]:

            pass_test(
                "2-hour and 1-hour sessions are on different days"
            )

        else:

            fail_test(
                "2-hour and 1-hour sessions are on different days",
                f"Found days: {days}"
            )

        # -----------------------------------------------------
        # Check total weekly hours
        # -----------------------------------------------------

        total_hours = sum(durations)

        if total_hours == 3:

            pass_test(
                "Total weekly course hours = 3"
            )

        else:

            fail_test(
                "Total weekly course hours = 3",
                f"Found {total_hours} hours."
            )

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    print()
    print("==============================")

    if passed:

        print(
            "2H + 1H SESSION VALIDATION PASSED"
        )

    else:

        print(
            "2H + 1H SESSION VALIDATION FAILED"
        )

finally:

    db.close()