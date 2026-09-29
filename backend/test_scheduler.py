from app.database import SessionLocal

from app.models.schedule import Schedule
from app.models.schedule_entry import ScheduleEntry
from app.models.course_requirement import CourseRequirement
from app.models.room import Room
from app.models.student_section import StudentSection
from app.models.time_slot import TimeSlot
from app.models.lecturer_availability import LecturerAvailability


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
    print("QINBIR Scheduler Validation")
    print("===========================")

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

    rooms = {
        room.id: room
        for room in db.query(Room).all()
    }

    sections = {
        section.id: section
        for section in db.query(StudentSection).all()
    }

    slots = {
        slot.id: slot
        for slot in db.query(TimeSlot).all()
    }

    unavailable_slots = {
        (
            availability.lecturer_id,
            availability.time_slot_id
        )
        for availability
        in db.query(LecturerAvailability).all()
        if not availability.is_available
    }

    # ---------------------------------------------------------
    # Test 1
    # Every requirement needs exactly 2 entries
    # ---------------------------------------------------------

    expected_entries = (
        len(requirements) * 2
    )

    if len(entries) == expected_entries:

        pass_test(
            f"Required sessions scheduled "
            f"({len(entries)}/{expected_entries})"
        )

    else:

        fail_test(
            "Required sessions scheduled",
            (
                f"Expected {expected_entries}, "
                f"but found {len(entries)}."
            )
        )

    # ---------------------------------------------------------
    # Test 2
    # Every requirement has exactly 2 entries
    # ---------------------------------------------------------

    requirement_entries = {}

    for entry in entries:

        requirement_entries.setdefault(
            entry.course_requirement_id,
            []
        ).append(entry)

    requirement_count_test = True

    for requirement in requirements:

        actual = len(
            requirement_entries.get(
                requirement.id,
                []
            )
        )

        if actual != 2:

            requirement_count_test = False

            print(
                f"  Requirement {requirement.id}: "
                f"expected 2 entries, found {actual}"
            )

    if requirement_count_test:

        pass_test(
            "Every course requirement has exactly 2 sessions"
        )

    else:

        fail_test(
            "Every course requirement has exactly 2 sessions"
        )

    # ---------------------------------------------------------
    # Test 3
    # Every requirement has exactly one 2-hour
    # and one 1-hour session
    # ---------------------------------------------------------

    duration_test = True

    for requirement in requirements:

        requirement_entries_list = requirement_entries.get(
            requirement.id,
            []
        )

        durations = []

        for entry in requirement_entries_list:

            slot = slots.get(entry.time_slot_id)

            if not slot:

                duration_test = False

                print(
                    f"  Entry {entry.id}: "
                    f"time slot {entry.time_slot_id} not found"
                )

                continue

            durations.append(slot_duration(slot))

        durations.sort()

        expected_durations = [1, 2]

        if durations != expected_durations:

            duration_test = False

            print(
                f"  Requirement {requirement.id}: "
                f"expected durations [1, 2], "
                f"found {durations}"
            )

    if duration_test:

        pass_test(
            "Every course has one 2-hour and one 1-hour session"
        )

    else:

        fail_test(
            "Every course has one 2-hour and one 1-hour session"
        )

    # ---------------------------------------------------------
    # Test 4
    # The 2-hour and 1-hour sessions must be on different days
    # ---------------------------------------------------------

    different_day_test = True

    for requirement in requirements:

        requirement_entries_list = requirement_entries.get(
            requirement.id,
            []
        )

        long_day = None
        short_day = None

        for entry in requirement_entries_list:

            slot = slots.get(entry.time_slot_id)

            if not slot:
                different_day_test = False
                continue

            duration = slot_duration(slot)

            if duration == 2:
                long_day = slot.day

            elif duration == 1:
                short_day = slot.day

        if long_day == short_day:

            different_day_test = False

            print(
                f"  Requirement {requirement.id}: "
                f"both sessions are on {long_day}"
            )

    if different_day_test:

        pass_test(
            "2-hour and 1-hour sessions are on different days"
        )

    else:

        fail_test(
            "2-hour and 1-hour sessions are on different days"
        )

    # ---------------------------------------------------------
    # Test 5
    # No room conflicts
    #
    # Slots can overlap even when their IDs are different.
    # Example:
    #
    # 08-10 overlaps 08-09 and 09-10.
    # ---------------------------------------------------------

    room_conflict = False

    for i, entry_a in enumerate(entries):

        slot_a = slots.get(entry_a.time_slot_id)

        if not slot_a:
            room_conflict = True
            continue

        a_start = (
            slot_a.start_time.hour * 60
            + slot_a.start_time.minute
        )

        a_end = (
            slot_a.end_time.hour * 60
            + slot_a.end_time.minute
        )

        for entry_b in entries[i + 1:]:

            if entry_a.room_id != entry_b.room_id:
                continue

            slot_b = slots.get(entry_b.time_slot_id)

            if not slot_b:
                room_conflict = True
                continue

            if slot_a.day != slot_b.day:
                continue

            b_start = (
                slot_b.start_time.hour * 60
                + slot_b.start_time.minute
            )

            b_end = (
                slot_b.end_time.hour * 60
                + slot_b.end_time.minute
            )

            overlap = (
                a_start < b_end
                and b_start < a_end
            )

            if overlap:

                room_conflict = True

                print(
                    f"  Room {entry_a.room_id}: "
                    f"entries {entry_a.id} and "
                    f"{entry_b.id} overlap"
                )

    if not room_conflict:

        pass_test("No room conflicts")

    else:

        fail_test("No room conflicts")

    # ---------------------------------------------------------
    # Test 6
    # No lecturer conflicts
    # ---------------------------------------------------------

    lecturer_conflict = False

    for i, entry_a in enumerate(entries):

        slot_a = slots.get(entry_a.time_slot_id)

        if not slot_a:
            lecturer_conflict = True
            continue

        a_start = (
            slot_a.start_time.hour * 60
            + slot_a.start_time.minute
        )

        a_end = (
            slot_a.end_time.hour * 60
            + slot_a.end_time.minute
        )

        for entry_b in entries[i + 1:]:

            if (
                entry_a.lecturer_id
                != entry_b.lecturer_id
            ):
                continue

            slot_b = slots.get(entry_b.time_slot_id)

            if not slot_b:
                lecturer_conflict = True
                continue

            if slot_a.day != slot_b.day:
                continue

            b_start = (
                slot_b.start_time.hour * 60
                + slot_b.start_time.minute
            )

            b_end = (
                slot_b.end_time.hour * 60
                + slot_b.end_time.minute
            )

            overlap = (
                a_start < b_end
                and b_start < a_end
            )

            if overlap:

                lecturer_conflict = True

                print(
                    f"  Lecturer {entry_a.lecturer_id}: "
                    f"entries {entry_a.id} and "
                    f"{entry_b.id} overlap"
                )

    if not lecturer_conflict:

        pass_test("No lecturer conflicts")

    else:

        fail_test("No lecturer conflicts")

    # ---------------------------------------------------------
    # Test 7
    # No student-section conflicts
    # ---------------------------------------------------------

    section_conflict = False

    for i, entry_a in enumerate(entries):

        slot_a = slots.get(entry_a.time_slot_id)

        if not slot_a:
            section_conflict = True
            continue

        a_start = (
            slot_a.start_time.hour * 60
            + slot_a.start_time.minute
        )

        a_end = (
            slot_a.end_time.hour * 60
            + slot_a.end_time.minute
        )

        for entry_b in entries[i + 1:]:

            if (
                entry_a.student_section_id
                != entry_b.student_section_id
            ):
                continue

            slot_b = slots.get(entry_b.time_slot_id)

            if not slot_b:
                section_conflict = True
                continue

            if slot_a.day != slot_b.day:
                continue

            b_start = (
                slot_b.start_time.hour * 60
                + slot_b.start_time.minute
            )

            b_end = (
                slot_b.end_time.hour * 60
                + slot_b.end_time.minute
            )

            overlap = (
                a_start < b_end
                and b_start < a_end
            )

            if overlap:

                section_conflict = True

                print(
                    f"  Student section "
                    f"{entry_a.student_section_id}: "
                    f"entries {entry_a.id} and "
                    f"{entry_b.id} overlap"
                )

    if not section_conflict:

        pass_test(
            "No student-section conflicts"
        )

    else:

        fail_test(
            "No student-section conflicts"
        )

    # ---------------------------------------------------------
    # Test 8
    # Room capacity
    # ---------------------------------------------------------

    capacity_error = False

    for entry in entries:

        room = rooms.get(entry.room_id)

        section = sections.get(
            entry.student_section_id
        )

        if not room or not section:

            capacity_error = True

            print(
                f"  Entry {entry.id}: "
                f"missing room or section"
            )

            continue

        if room.capacity < section.student_count:

            capacity_error = True

            print(
                f"  Entry {entry.id}: "
                f"room capacity {room.capacity} "
                f"< students "
                f"{section.student_count}"
            )

    if not capacity_error:

        pass_test(
            "Room capacity is sufficient"
        )

    else:

        fail_test(
            "Room capacity is sufficient"
        )

    # ---------------------------------------------------------
    # Test 9
    # Lecturer availability
    # ---------------------------------------------------------

    availability_error = False

    for entry in entries:

        key = (
            entry.lecturer_id,
            entry.time_slot_id
        )

        if key in unavailable_slots:

            availability_error = True

            print(
                f"  Entry {entry.id}: "
                f"lecturer {entry.lecturer_id} "
                f"is unavailable at "
                f"slot {entry.time_slot_id}"
            )

    if not availability_error:

        pass_test(
            "Lecturer availability is respected"
        )

    else:

        fail_test(
            "Lecturer availability is respected"
        )

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    print()
    print("===========================")
    print(
        f"Total schedule entries: "
        f"{len(entries)}"
    )

    if passed:

        print()
        print(
            "SCHEDULER VALIDATION PASSED"
        )

    else:

        print()
        print(
            "SCHEDULER VALIDATION FAILED"
        )

finally:

    db.close()