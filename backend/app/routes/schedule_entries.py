from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import case

from app.database import get_db

from app.models.schedule_entry import ScheduleEntry
from app.models.course_requirement import CourseRequirement
from app.models.course import Course
from app.models.lecturer import Lecturer
from app.models.student_section import StudentSection
from app.models.room import Room
from app.models.time_slot import TimeSlot


router = APIRouter(
    prefix="/schedule-entries",
    tags=["Schedule Entries"]
)


@router.get("/")
def get_schedule_entries(
    schedule_id: int | None = None,
    db: Session = Depends(get_db)
):

    query = (
        db.query(
            ScheduleEntry.id,
            ScheduleEntry.schedule_id,

            Course.code.label("course_code"),
            Course.name.label("course_name"),

            Lecturer.name.label("lecturer"),

            StudentSection.name.label(
                "student_section"
            ),

            StudentSection.student_count.label(
                "student_count"
            ),

            Room.name.label("room"),
            Room.capacity.label("room_capacity"),

            TimeSlot.day.label("day"),
            TimeSlot.start_time.label("start_time"),
            TimeSlot.end_time.label("end_time"),
        )

        .join(
            CourseRequirement,
            ScheduleEntry.course_requirement_id
            == CourseRequirement.id
        )

        .join(
            Course,
            CourseRequirement.course_id
            == Course.id
        )

        .join(
            Lecturer,
            ScheduleEntry.lecturer_id
            == Lecturer.id
        )

        .join(
            StudentSection,
            ScheduleEntry.student_section_id
            == StudentSection.id
        )

        .join(
            Room,
            ScheduleEntry.room_id
            == Room.id
        )

        .join(
            TimeSlot,
            ScheduleEntry.time_slot_id
            == TimeSlot.id
        )
    )

    # ==================================================
    # FILTER BY SCHEDULE
    # ==================================================

    if schedule_id is not None:

        query = query.filter(
            ScheduleEntry.schedule_id
            == schedule_id
        )

    # ==================================================
    # SORT DAYS IN UNIVERSITY ORDER
    # ==================================================

    day_order = case(
        (TimeSlot.day == "Monday", 1),
        (TimeSlot.day == "Tuesday", 2),
        (TimeSlot.day == "Wednesday", 3),
        (TimeSlot.day == "Thursday", 4),
        (TimeSlot.day == "Friday", 5),
        (TimeSlot.day == "Saturday", 6),
        (TimeSlot.day == "Sunday", 7),
        else_=8
    )

    entries = query.order_by(
        day_order,
        TimeSlot.start_time
    ).all()

    # ==================================================
    # FORMAT RESPONSE
    # ==================================================

    result = []

    for entry in entries:

        result.append({

            "id": entry.id,

            "schedule_id": entry.schedule_id,

            "course": (
                f"{entry.course_code} - "
                f"{entry.course_name}"
            ),

            "lecturer": entry.lecturer,

            "student_section": (
                entry.student_section
            ),

            "student_count": (
                entry.student_count
            ),

            "room": entry.room,

            "room_capacity": (
                entry.room_capacity
            ),

            "day": entry.day,

            "start_time": (
                entry.start_time.strftime("%H:%M")
            ),

            "end_time": (
                entry.end_time.strftime("%H:%M")
            ),
        })

    return result