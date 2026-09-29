from pulp import (
    LpProblem,
    LpVariable,
    lpSum,
    LpBinary,
    LpMinimize,
    LpStatus,
)

from app.database import SessionLocal

from app.models.course_requirement import CourseRequirement
from app.models.course import Course
from app.models.room import Room
from app.models.time_slot import TimeSlot
from app.models.student_section import StudentSection
from app.models.lecturer import Lecturer
from app.models.lecturer_availability import LecturerAvailability
from app.models.schedule import Schedule
from app.models.schedule_entry import ScheduleEntry


def slot_duration(slot):
    """Return the duration of a time slot in hours."""

    start_minutes = (
        slot.start_time.hour * 60
        + slot.start_time.minute
    )

    end_minutes = (
        slot.end_time.hour * 60
        + slot.end_time.minute
    )

    return (end_minutes - start_minutes) / 60


def create_schedule():

    print()
    print("QINBIR Scheduler")
    print("================")

    db = SessionLocal()

    try:

        course_requirements = db.query(
            CourseRequirement
        ).all()

        courses = db.query(Course).all()
        lecturers = db.query(Lecturer).all()
        rooms = db.query(Room).all()
        time_slots = db.query(TimeSlot).all()
        student_sections = db.query(StudentSection).all()

        lecturer_availability = db.query(
            LecturerAvailability
        ).all()

        print(
            f"Course requirements: "
            f"{len(course_requirements)}"
        )

        print(f"Rooms: {len(rooms)}")
        print(f"Time slots: {len(time_slots)}")
        print(
            f"Student sections: "
            f"{len(student_sections)}"
        )

        print(
            f"Lecturer availability records: "
            f"{len(lecturer_availability)}"
        )

        # ---------------------------------------------------------
        # Basic validation
        # ---------------------------------------------------------

        if not course_requirements:
            print("No course requirements found.")

            return {
                "status": "error",
                "message": "No course requirements found.",
            }

        if not rooms:
            print("No rooms found.")

            return {
                "status": "error",
                "message": "No rooms found.",
            }

        if not time_slots:
            print("No time slots found.")

            return {
                "status": "error",
                "message": "No time slots found.",
            }

        if not student_sections:
            print("No student sections found.")

            return {
                "status": "error",
                "message": "No student sections found.",
            }

        # ---------------------------------------------------------
        # Separate 1-hour and 2-hour slots
        # ---------------------------------------------------------

        two_hour_slots = [
            slot
            for slot in time_slots
            if slot_duration(slot) == 2
        ]

        one_hour_slots = [
            slot
            for slot in time_slots
            if slot_duration(slot) == 1
        ]

        print(
            f"2-hour slots: "
            f"{len(two_hour_slots)}"
        )

        print(
            f"1-hour slots: "
            f"{len(one_hour_slots)}"
        )

        # ---------------------------------------------------------
        # Create optimization problem
        # ---------------------------------------------------------

        problem = LpProblem(
            "QINBIR_Course_Scheduling",
            LpMinimize
        )

        assignments = {}

        # ---------------------------------------------------------
        # Create assignment variables
        #
        # Session 0 = 2-hour session
        # Session 1 = 1-hour session
        # ---------------------------------------------------------

        for requirement in course_requirements:

            for session_number in range(2):

                if session_number == 0:

                    allowed_slots = [
                        slot
                        for slot in two_hour_slots
                        if requirement.long_session_hours == 2
                    ]

                else:

                    allowed_slots = [
                        slot
                        for slot in one_hour_slots
                        if requirement.short_session_hours == 1
                    ]

                for room in rooms:

                    for slot in allowed_slots:

                        key = (
                            requirement.id,
                            session_number,
                            room.id,
                            slot.id,
                        )

                        assignments[key] = LpVariable(
                            (
                                f"assign_"
                                f"{requirement.id}_"
                                f"{session_number}_"
                                f"{room.id}_"
                                f"{slot.id}"
                            ),
                            cat=LpBinary,
                        )

        # ---------------------------------------------------------
        # Constraint 1
        #
        # Every course requirement must have:
        # exactly one 2-hour session
        # exactly one 1-hour session
        # ---------------------------------------------------------

        for requirement in course_requirements:

            for session_number in range(2):

                problem += (
                    lpSum(
                        variable
                        for key, variable
                        in assignments.items()
                        if key[0] == requirement.id
                        and key[1] == session_number
                    )
                    == 1
                )

        # ---------------------------------------------------------
        # Constraint 2
        #
        # Room conflict
        # ---------------------------------------------------------

        for room in rooms:

            for day in set(
                slot.day
                for slot in time_slots
            ):

                for slot_a in time_slots:

                    for slot_b in time_slots:

                        if slot_a.id == slot_b.id:
                            continue

                        if (
                            slot_a.day != day
                            or slot_b.day != day
                        ):
                            continue

                        a_start = (
                            slot_a.start_time.hour * 60
                            + slot_a.start_time.minute
                        )

                        a_end = (
                            slot_a.end_time.hour * 60
                            + slot_a.end_time.minute
                        )

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

                        if not overlap:
                            continue

                        relevant_variables = []

                        for key, variable in assignments.items():

                            room_id = key[2]
                            slot_id = key[3]

                            if room_id != room.id:
                                continue

                            if slot_id not in (
                                slot_a.id,
                                slot_b.id
                            ):
                                continue

                            relevant_variables.append(
                                variable
                            )

                        if relevant_variables:

                            problem += (
                                lpSum(
                                    relevant_variables
                                )
                                <= 1
                            )

        # ---------------------------------------------------------
        # Constraint 3
        #
        # Lecturer conflict
        # ---------------------------------------------------------

        for lecturer_id in set(
            requirement.lecturer_id
            for requirement in course_requirements
        ):

            for day in set(
                slot.day
                for slot in time_slots
            ):

                for slot_a in time_slots:

                    if slot_a.day != day:
                        continue

                    a_start = (
                        slot_a.start_time.hour * 60
                        + slot_a.start_time.minute
                    )

                    a_end = (
                        slot_a.end_time.hour * 60
                        + slot_a.end_time.minute
                    )

                    overlapping_slots = []

                    for slot_b in time_slots:

                        if slot_b.day != day:
                            continue

                        b_start = (
                            slot_b.start_time.hour * 60
                            + slot_b.start_time.minute
                        )

                        b_end = (
                            slot_b.end_time.hour * 60
                            + slot_b.end_time.minute
                        )

                        if (
                            a_start < b_end
                            and b_start < a_end
                        ):

                            overlapping_slots.append(
                                slot_b.id
                            )

                    relevant_variables = []

                    for key, variable in assignments.items():

                        requirement_id = key[0]
                        slot_id = key[3]

                        requirement = next(
                            r
                            for r in course_requirements
                            if r.id == requirement_id
                        )

                        if (
                            requirement.lecturer_id
                            != lecturer_id
                        ):
                            continue

                        if slot_id in overlapping_slots:

                            relevant_variables.append(
                                variable
                            )

                    if relevant_variables:

                        problem += (
                            lpSum(
                                relevant_variables
                            )
                            <= 1
                        )

        # ---------------------------------------------------------
        # Constraint 4
        #
        # Student section conflict
        # ---------------------------------------------------------

        for section_id in set(
            requirement.student_section_id
            for requirement in course_requirements
        ):

            for day in set(
                slot.day
                for slot in time_slots
            ):

                for slot_a in time_slots:

                    if slot_a.day != day:
                        continue

                    a_start = (
                        slot_a.start_time.hour * 60
                        + slot_a.start_time.minute
                    )

                    a_end = (
                        slot_a.end_time.hour * 60
                        + slot_a.end_time.minute
                    )

                    overlapping_slots = []

                    for slot_b in time_slots:

                        if slot_b.day != day:
                            continue

                        b_start = (
                            slot_b.start_time.hour * 60
                            + slot_b.start_time.minute
                        )

                        b_end = (
                            slot_b.end_time.hour * 60
                            + slot_b.end_time.minute
                        )

                        if (
                            a_start < b_end
                            and b_start < a_end
                        ):

                            overlapping_slots.append(
                                slot_b.id
                            )

                    relevant_variables = []

                    for key, variable in assignments.items():

                        requirement_id = key[0]
                        slot_id = key[3]

                        requirement = next(
                            r
                            for r in course_requirements
                            if r.id == requirement_id
                        )

                        if (
                            requirement.student_section_id
                            != section_id
                        ):
                            continue

                        if slot_id in overlapping_slots:

                            relevant_variables.append(
                                variable
                            )

                    if relevant_variables:

                        problem += (
                            lpSum(
                                relevant_variables
                            )
                            <= 1
                        )

        # ---------------------------------------------------------
        # Constraint 5
        #
        # Room capacity
        # ---------------------------------------------------------

        for requirement in course_requirements:

            section = next(
                (
                    s
                    for s in student_sections
                    if s.id
                    == requirement.student_section_id
                ),
                None,
            )

            if section is None:

                print(
                    f"Student section "
                    f"{requirement.student_section_id} "
                    f"not found."
                )

                return {
                    "status": "error",
                    "message": (
                        "Student section not found."
                    ),
                }

            for key, variable in assignments.items():

                if key[0] != requirement.id:
                    continue

                room_id = key[2]

                room = next(
                    r
                    for r in rooms
                    if r.id == room_id
                )

                if (
                    room.capacity
                    < section.student_count
                ):

                    problem += variable == 0

        # ---------------------------------------------------------
        # Constraint 6
        #
        # Lecturer availability
        # ---------------------------------------------------------

        unavailable_slots = set()

        for availability in lecturer_availability:

            if not availability.is_available:

                unavailable_slots.add(
                    (
                        availability.lecturer_id,
                        availability.time_slot_id
                    )
                )

        for key, variable in assignments.items():

            requirement_id = key[0]
            slot_id = key[3]

            requirement = next(
                r
                for r in course_requirements
                if r.id == requirement_id
            )

            if (
                requirement.lecturer_id,
                slot_id
            ) in unavailable_slots:

                problem += variable == 0

        # ---------------------------------------------------------
        # Constraint 7
        #
        # 2-hour and 1-hour sessions of the same requirement
        # must be on different days.
        # ---------------------------------------------------------

        for requirement in course_requirements:

            for day in set(
                slot.day
                for slot in time_slots
            ):

                long_variables = [
                    variable
                    for key, variable
                    in assignments.items()
                    if (
                        key[0] == requirement.id
                        and key[1] == 0
                        and any(
                            slot.id == key[3]
                            and slot.day == day
                            for slot in two_hour_slots
                        )
                    )
                ]

                short_variables = [
                    variable
                    for key, variable
                    in assignments.items()
                    if (
                        key[0] == requirement.id
                        and key[1] == 1
                        and any(
                            slot.id == key[3]
                            and slot.day == day
                            for slot in one_hour_slots
                        )
                    )
                ]

                if (
                    long_variables
                    and short_variables
                ):

                    problem += (
                        lpSum(long_variables)
                        + lpSum(short_variables)
                        <= 1
                    )

        # ---------------------------------------------------------
        # Objective
        #
        # We are finding a valid timetable.
        # ---------------------------------------------------------

        problem += 0

        # ---------------------------------------------------------
        # Solve
        # ---------------------------------------------------------

        status = problem.solve()

        print()
        print(
            f"Solver status: "
            f"{LpStatus[status]}"
        )

        # ---------------------------------------------------------
        # Infeasible / failed schedule
        # ---------------------------------------------------------

        if LpStatus[status] != "Optimal":

            print(
                "No valid schedule found."
            )

            return {
                "status": "infeasible",
                "message": "No valid schedule found.",
            }

        # ---------------------------------------------------------
        # Remove previous automatic draft
        # ---------------------------------------------------------

        old_schedule = (
            db.query(Schedule)
            .filter(
                Schedule.name
                == "Automatically Generated Schedule",
                Schedule.status == "DRAFT",
            )
            .first()
        )

        if old_schedule:

            print()
            print(
                "Removing previous automatic "
                "draft schedule..."
            )

            db.query(ScheduleEntry).filter(
                ScheduleEntry.schedule_id
                == old_schedule.id
            ).delete(
                synchronize_session=False
            )

            db.delete(old_schedule)

            db.commit()

            print(
                "Previous automatic schedule removed."
            )

        # ---------------------------------------------------------
        # Create new schedule
        # ---------------------------------------------------------

        schedule = Schedule(
            name="Automatically Generated Schedule",
            status="DRAFT",
        )

        db.add(schedule)

        db.commit()

        db.refresh(schedule)

        print()
        print(
            "Schedule created successfully."
        )

        print(
            f"Schedule ID: "
            f"{schedule.id}"
        )

        saved_entries = 0

        print()
        print("Generated Schedule")
        print("==================")

        # ---------------------------------------------------------
        # Save selected assignments
        # ---------------------------------------------------------

        for key, variable in assignments.items():

            if variable.value() != 1:
                continue

            (
                requirement_id,
                session_number,
                room_id,
                slot_id,
            ) = key

            requirement = next(
                r
                for r in course_requirements
                if r.id == requirement_id
            )

            room = next(
                r
                for r in rooms
                if r.id == room_id
            )

            slot = next(
                s
                for s in time_slots
                if s.id == slot_id
            )

            section = next(
                s
                for s in student_sections
                if s.id
                == requirement.student_section_id
            )

            course = next(
                c
                for c in courses
                if c.id == requirement.course_id
            )

            lecturer = next(
                l
                for l in lecturers
                if l.id == requirement.lecturer_id
            )

            duration = slot_duration(slot)

            schedule_entry = ScheduleEntry(
                schedule_id=schedule.id,
                course_requirement_id=requirement.id,
                lecturer_id=requirement.lecturer_id,
                student_section_id=requirement.student_section_id,
                room_id=room.id,
                time_slot_id=slot.id,
            )

            db.add(schedule_entry)

            saved_entries += 1

            session_type = (
                "2-hour session"
                if session_number == 0
                else "1-hour session"
            )

            print()
            print(
                f"Course: "
                f"{course.code} - "
                f"{course.name}"
            )

            print(
                f"Session: "
                f"{session_type}"
            )

            print(
                f"Duration: "
                f"{duration:g} hour(s)"
            )

            print(
                f"Lecturer: "
                f"{lecturer.name}"
            )

            print(
                f"Student Section: "
                f"{section.name}"
            )

            print(
                f"Students: "
                f"{section.student_count}"
            )

            print(
                f"Room: "
                f"{room.name}"
            )

            print(
                f"Room Capacity: "
                f"{room.capacity}"
            )

            print(
                f"Time: "
                f"{slot.day} "
                f"{slot.start_time} - "
                f"{slot.end_time}"
            )

        # ---------------------------------------------------------
        # Save schedule entries
        # ---------------------------------------------------------

        db.commit()

        print()
        print(
            "Schedule entries saved successfully."
        )

        print(
            f"Total entries saved: "
            f"{saved_entries}"
        )

        # ---------------------------------------------------------
        # Return result for FastAPI
        # ---------------------------------------------------------

        return {
            "status": "success",
            "schedule_id": schedule.id,
            "entries_created": saved_entries,
        }

    except Exception as e:

        db.rollback()

        print()
        print("Scheduler error:")
        print(e)

        return {
            "status": "error",
            "message": str(e),
        }

    finally:

        db.close()


if __name__ == "__main__":
    create_schedule()