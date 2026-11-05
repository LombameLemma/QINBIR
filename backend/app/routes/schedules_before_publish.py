from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.schedule import Schedule
from app.models.schedule_entry import ScheduleEntry
from app.models.course_requirement import CourseRequirement
from app.models.course import Course
from app.models.lecturer import Lecturer
from app.models.student_section import StudentSection
from app.models.room import Room
from app.models.time_slot import TimeSlot

from scheduler.scheduler import create_schedule


router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"]
)


# ==================================================
# GET ALL SCHEDULES
# ==================================================

@router.get("/")
def get_schedules(
    db: Session = Depends(get_db)
):

    schedules = db.query(Schedule).all()

    return schedules


# ==================================================
# GET ONE COMPLETE SCHEDULE
# ==================================================

@router.get("/{schedule_id}")
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):

    # ----------------------------------------------
    # Find schedule
    # ----------------------------------------------

    schedule = (
        db.query(Schedule)
        .filter(
            Schedule.id == schedule_id
        )
        .first()
    )

    if not schedule:

        raise HTTPException(
            status_code=404,
            detail="Schedule not found."
        )


    # ----------------------------------------------
    # Get readable schedule entries
    # ----------------------------------------------

    entries = (
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

        .filter(
            ScheduleEntry.schedule_id
            == schedule_id
        )

        .order_by(
            TimeSlot.day,
            TimeSlot.start_time
        )

        .all()
    )


    # ----------------------------------------------
    # Convert database rows to readable JSON
    # ----------------------------------------------

    readable_entries = []

    for entry in entries:

        readable_entries.append({

            "id": entry.id,

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


    # ----------------------------------------------
    # Return complete schedule
    # ----------------------------------------------

    return {

        "schedule": {

            "id": schedule.id,

            "name": schedule.name,

            "status": schedule.status,

            "created_at": schedule.created_at,

            "approved_at": schedule.approved_at,

            "published_at": schedule.published_at,
        },

        "entries": readable_entries,

        "entries_count": len(
            readable_entries
        ),
    }


# ==================================================
# GENERATE NEW SCHEDULE
# ==================================================

@router.post("/generate")
def generate_schedule(
    db: Session = Depends(get_db)
):

    try:

        create_schedule()


        # ------------------------------------------
        # Find newly generated schedule
        # ------------------------------------------

        schedule = (
            db.query(Schedule)
            .filter(
                Schedule.name
                == "Automatically Generated Schedule",

                Schedule.status
                == "DRAFT",
            )

            .order_by(
                Schedule.id.desc()
            )

            .first()
        )


        if not schedule:

            raise HTTPException(
                status_code=500,
                detail="Schedule generation failed."
            )


        # ------------------------------------------
        # Count generated entries
        # ------------------------------------------

        entries = (
            db.query(ScheduleEntry)
            .filter(
                ScheduleEntry.schedule_id
                == schedule.id
            )
            .all()
        )


        return {

            "message":
                "Schedule generated successfully.",

            "schedule_id":
                schedule.id,

            "status":
                schedule.status,

            "entries_created":
                len(entries),
        }


    except HTTPException:

        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )