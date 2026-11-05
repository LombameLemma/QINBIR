from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import case
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.lecturer import Lecturer
from app.models.schedule import Schedule
from app.models.schedule_entry import ScheduleEntry
from app.models.course_requirement import CourseRequirement
from app.models.course import Course
from app.models.student_section import StudentSection
from app.models.room import Room
from app.models.time_slot import TimeSlot
from app.security import require_role


router = APIRouter(
    prefix="/timetable",
    tags=["Personal Timetable"],
)


@router.get("/lecturer/me")
def get_my_lecturer_timetable(
    current_user: User = Depends(require_role("LECTURER")),
    db: Session = Depends(get_db),
):
    lecturer = (
        db.query(Lecturer)
        .filter(Lecturer.user_id == current_user.id)
        .first()
    )

    if lecturer is None:
        raise HTTPException(
            status_code=404,
            detail="No lecturer profile is linked to this account.",
        )

    day_order = case(
        (TimeSlot.day == "Monday", 1),
        (TimeSlot.day == "Tuesday", 2),
        (TimeSlot.day == "Wednesday", 3),
        (TimeSlot.day == "Thursday", 4),
        (TimeSlot.day == "Friday", 5),
        (TimeSlot.day == "Saturday", 6),
        (TimeSlot.day == "Sunday", 7),
        else_=8,
    )

    entries = (
        db.query(
            ScheduleEntry.id,
            Schedule.id.label("schedule_id"),
            Schedule.name.label("schedule_name"),
            Course.code.label("course_code"),
            Course.name.label("course_name"),
            StudentSection.name.label("student_section"),
            Room.name.label("room"),
            TimeSlot.day.label("day"),
            TimeSlot.start_time.label("start_time"),
            TimeSlot.end_time.label("end_time"),
        )
        .join(Schedule, ScheduleEntry.schedule_id == Schedule.id)
        .join(
            CourseRequirement,
            ScheduleEntry.course_requirement_id == CourseRequirement.id,
        )
        .join(Course, CourseRequirement.course_id == Course.id)
        .join(
            StudentSection,
            ScheduleEntry.student_section_id == StudentSection.id,
        )
        .join(Room, ScheduleEntry.room_id == Room.id)
        .join(TimeSlot, ScheduleEntry.time_slot_id == TimeSlot.id)
        .filter(
            ScheduleEntry.lecturer_id == lecturer.id,
            Schedule.status == "PUBLISHED",
            Schedule.published_at.isnot(None),
        )
        .order_by(day_order, TimeSlot.start_time)
        .all()
    )

    return {
        "lecturer": lecturer.name,
        "entries": [
            {
                "id": entry.id,
                "schedule_id": entry.schedule_id,
                "schedule_name": entry.schedule_name,
                "course": f"{entry.course_code} - {entry.course_name}",
                "student_section": entry.student_section,
                "room": entry.room,
                "day": entry.day,
                "start_time": entry.start_time.strftime("%H:%M"),
                "end_time": entry.end_time.strftime("%H:%M"),
            }
            for entry in entries
        ],
        "entries_count": len(entries),
    }
