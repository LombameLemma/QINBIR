from app.database import SessionLocal

from app.models.schedule import Schedule
from app.models.schedule_entry import ScheduleEntry
from app.models.course_requirement import CourseRequirement
from app.models.lecturer import Lecturer
from app.models.student_section import StudentSection
from app.models.room import Room
from app.models.time_slot import TimeSlot


db = SessionLocal()

try:
    # 1. Get existing data
    course_requirement = db.query(CourseRequirement).first()
    lecturer = db.query(Lecturer).first()
    section = db.query(StudentSection).first()
    room = db.query(Room).first()
    time_slot = db.query(TimeSlot).first()

    # 2. Create a Schedule
    schedule = Schedule(
        name="Semester 1 - 2026/2027",
        status="DRAFT"
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    # 3. Create a Schedule Entry
    entry = ScheduleEntry(
        schedule_id=schedule.id,
        course_requirement_id=course_requirement.id,
        lecturer_id=lecturer.id,
        student_section_id=section.id,
        room_id=room.id,
        time_slot_id=time_slot.id
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    print()
    print("Schedule created successfully!")
    print()
    print(f"Schedule: {schedule.name}")
    print(f"Status: {schedule.status}")
    print()
    print("Schedule Entry:")
    print(f"Course: {course_requirement.course_id}")
    print(f"Lecturer: {lecturer.name}")
    print(f"Section: {section.name}")
    print(f"Room: {room.name}")
    print(
        f"Time: {time_slot.day} "
        f"{time_slot.start_time} - {time_slot.end_time}"
    )

finally:
    db.close()