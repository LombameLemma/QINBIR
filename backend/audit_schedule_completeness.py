
from collections import defaultdict

from app.database import SessionLocal
from app.models.schedule import Schedule
from app.models.schedule_entry import ScheduleEntry
from app.models.course_requirement import CourseRequirement
from app.models.course import Course
from app.models.time_slot import TimeSlot

SCHEDULE_ID = 1

db = SessionLocal()

try:
    schedule = db.query(Schedule).filter(
        Schedule.id == SCHEDULE_ID
    ).first()

    if schedule is None:
        raise RuntimeError("Schedule not found.")

    requirements = (
        db.query(CourseRequirement, Course)
        .join(Course, CourseRequirement.course_id == Course.id)
        .all()
    )

    entries = (
        db.query(ScheduleEntry, TimeSlot)
        .join(TimeSlot, ScheduleEntry.time_slot_id == TimeSlot.id)
        .filter(ScheduleEntry.schedule_id == SCHEDULE_ID)
        .all()
    )

    grouped = defaultdict(list)

    for entry, slot in entries:
        grouped[entry.course_requirement_id].append(
            (entry, slot)
        )

    requirement_ids = {
        requirement.id for requirement, course in requirements
    }

    scheduled_ids = set(grouped.keys())

    missing = requirement_ids - scheduled_ids
    unknown = scheduled_ids - requirement_ids

    problems = []

    for requirement, course in requirements:
        sessions = grouped.get(requirement.id, [])

        durations = [
            (slot.end_time.hour * 60 + slot.end_time.minute)
            - (slot.start_time.hour * 60 + slot.start_time.minute)
            for entry, slot in sessions
        ]

        days = {slot.day for entry, slot in sessions}

        credits = course.credit_hours

        if credits == 2:
            valid = len(sessions) == 1 and durations == [120]

        elif credits == 3:
            valid = (
                len(sessions) == 2
                and sorted(durations) == [60, 120]
                and len(days) == 2
            )

        elif credits == 4:
            valid = (
                len(sessions) == 2
                and durations == [120, 120]
                and len(days) == 2
            )

        else:
            valid = False

        if not valid:
            problems.append(
                f"Requirement {requirement.id}: "
                f"{course.code}, {credits} credits, "
                f"{len(sessions)} sessions, durations={durations}, "
                f"days={sorted(days)}"
            )

    duplicate_requirements = {
        requirement_id: len(sessions)
        for requirement_id, sessions in grouped.items()
        if len(sessions) > 2
    }

    print("\n========== SCHEDULE COMPLETENESS AUDIT ==========")
    print(f"Schedule ID: {schedule.id}")
    print(f"Schedule status: {schedule.status}")
    print(f"Total course requirements: {len(requirements)}")
    print(f"Total schedule entries: {len(entries)}")
    print(f"Requirements represented: {len(scheduled_ids)}")
    print(f"Missing requirements: {len(missing)}")
    print(f"Unknown requirement IDs: {len(unknown)}")
    print(f"Requirements with invalid session patterns: {len(problems)}")

    if missing:
        print("\nMISSING REQUIREMENT IDS:")
        for requirement_id in sorted(missing):
            print("-", requirement_id)

    if unknown:
        print("\nUNKNOWN REQUIREMENT IDS:")
        for requirement_id in sorted(unknown):
            print("-", requirement_id)

    if problems:
        print("\nINVALID SESSION PATTERNS:")
        for problem in problems:
            print("-", problem)

    if duplicate_requirements:
        print("\nREQUIREMENTS WITH MORE THAN TWO ENTRIES:")
        for requirement_id, count in sorted(
            duplicate_requirements.items()
        ):
            print(f"- Requirement {requirement_id}: {count} entries")

    if not missing and not unknown and not problems:
        print("\nPASS: All requirements have valid session patterns.")
    else:
        print("\nAUDIT RESULT: REVIEW REQUIRED.")

finally:
    db.close()
