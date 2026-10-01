from pathlib import Path
import shutil

from app.database import Base, engine, SessionLocal

# Import every model so SQLAlchemy knows all tables
from app.models.user import User
from app.models.department import Department
from app.models.program import Program
from app.models.program_course import ProgramCourse
from app.models.course import Course
from app.models.lecturer import Lecturer
from app.models.student_section import StudentSection
from app.models.room import Room
from app.models.time_slot import TimeSlot
from app.models.lecturer_availability import LecturerAvailability
from app.models.course_requirement import CourseRequirement
from app.models.schedule import Schedule
from app.models.schedule_entry import ScheduleEntry
from app.models.constraint import Constraint


# ============================================================
# DATABASE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "qinbir.db"
BACKUP_PATH = BASE_DIR / "qinbir_backup_before_small_sample.db"


# ============================================================
# BACKUP CURRENT DATABASE
# ============================================================

print("=" * 60)
print("QINBIR SMALL SAMPLE DATABASE RESET")
print("=" * 60)

if DB_PATH.exists():

    if BACKUP_PATH.exists():
        BACKUP_PATH.unlink()

    shutil.copy2(DB_PATH, BACKUP_PATH)

    print()
    print("Backup created:")
    print(BACKUP_PATH)

else:
    print()
    print("WARNING: Current database does not exist.")


# ============================================================
# RESET DATABASE
# ============================================================

print()
print("Removing old database tables...")

Base.metadata.drop_all(bind=engine)

print("Creating fresh database tables...")

Base.metadata.create_all(bind=engine)


# ============================================================
# DATABASE SESSION
# ============================================================

db = SessionLocal()


try:

    # ========================================================
    # DEPARTMENTS
    # ========================================================

    departments_data = [
        ("Computational and Natural Science", "CNS"),
        ("Social Science", "SS"),
        ("Health", "HLT"),
        ("Institute of Technology", "IOT"),
    ]

    departments = []

    for name, code in departments_data:
        department = Department(
            name=name,
            code=code,
        )

        db.add(department)
        departments.append(department)

    db.flush()


    # ========================================================
    # PROGRAMS
    # ========================================================

    programs_data = [
        ("Computer Science", "CS", departments[0].id),
        ("Information Systems", "IS", departments[0].id),
        ("Mathematics", "MATH", departments[0].id),

        ("Economics", "ECON", departments[1].id),
        ("Management", "MGT", departments[1].id),

        ("Public Health", "PH", departments[2].id),
        ("Nursing", "NUR", departments[2].id),

        ("Software Engineering", "SE", departments[3].id),
        ("Information Technology", "IT", departments[3].id),
        ("Computer Engineering", "CE", departments[3].id),
    ]

    programs = []

    for name, code, department_id in programs_data:
        program = Program(
            name=name,
            code=code,
            department_id=department_id,
        )

        db.add(program)
        programs.append(program)

    db.flush()


    # ========================================================
    # COURSES
    # ========================================================

    courses_data = [
        ("CS101", "Introduction to Programming", 3),
        ("CS102", "Data Structures", 3),
        ("IS101", "Information Systems", 3),
        ("MATH101", "Calculus I", 2),
        ("ECON101", "Principles of Economics", 3),
        ("MGT101", "Principles of Management", 2),
        ("PH101", "Introduction to Public Health", 3),
        ("NUR101", "Fundamentals of Nursing", 3),
        ("SE101", "Software Engineering Fundamentals", 3),
        ("IT101", "Introduction to Information Technology", 2),
    ]

    courses = []

    for code, name, credit_hours in courses_data:
        course = Course(
            code=code,
            name=name,
            credit_hours=credit_hours,
        )

        db.add(course)
        courses.append(course)

    db.flush()


    # ========================================================
    # PROGRAM-COURSE RELATIONSHIPS
    # ========================================================

    program_course_pairs = [
        (0, 0),   # CS -> CS101
        (0, 1),   # CS -> CS102
        (1, 2),   # IS -> IS101
        (2, 3),   # MATH -> MATH101
        (3, 4),   # ECON -> ECON101
        (4, 5),   # MGT -> MGT101
        (5, 6),   # PH -> PH101
        (6, 7),   # NUR -> NUR101
        (7, 8),   # SE -> SE101
        (8, 9),   # IT -> IT101
    ]

    for program_index, course_index in program_course_pairs:

        relationship = ProgramCourse(
            program_id=programs[program_index].id,
            course_id=courses[course_index].id,
        )

        db.add(relationship)


    # ========================================================
    # USERS
    # ========================================================

    users = []

    for i in range(1, 11):

        user = User(
            full_name=f"Lecturer {i}",
            email=f"lecturer{i}@qinbir.edu.et",
            password_hash="sample_password_hash",
            role="LECTURER",
            is_active=True,
        )

        db.add(user)
        users.append(user)

    db.flush()


    # ========================================================
    # LECTURERS
    # ========================================================

    lecturers = []

    for i in range(10):

        lecturer = Lecturer(
            user_id=users[i].id,
            department_id=departments[i % 4].id,
            employee_id=f"EMP{i + 1:03d}",
            name=f"Lecturer {i + 1}",
        )

        db.add(lecturer)
        lecturers.append(lecturer)

    db.flush()


    # ========================================================
    # STUDENT SECTIONS
    # ========================================================

    sections = []

    for i in range(10):

        section = StudentSection(
            name=f"SECTION-{i + 1}",
            program_id=programs[i].id,
            year=2,
            semester=1,
            student_count=40,
        )

        db.add(section)
        sections.append(section)

    db.flush()


    # ========================================================
    # ROOMS
    # ========================================================

    rooms = []

    for i in range(1, 11):

        room = Room(
            name=f"ROOM-{i}",
            building="Main Building",
            capacity=60,
            room_type="CLASSROOM",
        )

        db.add(room)
        rooms.append(room)

    db.flush()


    # ========================================================
    # TIME SLOTS
    # ========================================================

    time_slots_data = [
        ("Monday", "08:00", "10:00"),
        ("Monday", "10:00", "11:00"),

        ("Tuesday", "08:00", "10:00"),
        ("Tuesday", "10:00", "11:00"),

        ("Wednesday", "08:00", "10:00"),
        ("Wednesday", "10:00", "11:00"),

        ("Thursday", "08:00", "10:00"),
        ("Thursday", "10:00", "11:00"),

        ("Friday", "08:00", "10:00"),
        ("Friday", "10:00", "11:00"),
    ]

    from datetime import time

    time_slots = []

    for day, start, end in time_slots_data:

        start_hour, start_minute = map(int, start.split(":"))
        end_hour, end_minute = map(int, end.split(":"))

        slot = TimeSlot(
            day=day,
            start_time=time(start_hour, start_minute),
            end_time=time(end_hour, end_minute),
        )

        db.add(slot)
        time_slots.append(slot)

    db.flush()


    # ========================================================
    # LECTURER AVAILABILITY
    # ========================================================

    availability_count = 0

    for lecturer in lecturers:

        for slot in time_slots:

            availability = LecturerAvailability(
                lecturer_id=lecturer.id,
                time_slot_id=slot.id,
                is_available=True,
            )

            db.add(availability)

            availability_count += 1


    # ========================================================
    # COURSE REQUIREMENTS
    # ========================================================

    requirements = []

    for i in range(10):

        course = courses[i]

        if course.credit_hours == 2:
            sessions_per_week = 1
        else:
            sessions_per_week = 2

        requirement = CourseRequirement(
            course_id=course.id,
            student_section_id=sections[i].id,
            lecturer_id=lecturers[i].id,
            sessions_per_week=sessions_per_week,
            long_session_hours=2,
            short_session_hours=1,
        )

        db.add(requirement)
        requirements.append(requirement)


    # ========================================================
    # SAVE EVERYTHING
    # ========================================================

    db.commit()


    # ========================================================
    # FINAL COUNTS
    # ========================================================

    print()
    print("=" * 60)
    print("SMALL SAMPLE DATABASE CREATED")
    print("=" * 60)

    print(f"Departments:          {len(departments)}")
    print(f"Programs:             {len(programs)}")
    print(f"Courses:              {len(courses)}")
    print(f"Users:                {len(users)}")
    print(f"Lecturers:            {len(lecturers)}")
    print(f"Student Sections:     {len(sections)}")
    print(f"Rooms:                {len(rooms)}")
    print(f"Time Slots:           {len(time_slots)}")
    print(f"Availability:         {availability_count}")
    print(f"Requirements:         {len(requirements)}")

    print()
    print("Backup:")
    print(BACKUP_PATH)

    print()
    print("Reset completed successfully.")


except Exception as error:

    db.rollback()

    print()
    print("=" * 60)
    print("ERROR")
    print("=" * 60)

    print(error)

    raise


finally:

    db.close()