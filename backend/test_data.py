from datetime import time

from app.database import SessionLocal

from app.models.user import User
from app.models.department import Department
from app.models.program import Program
from app.models.course import Course
from app.models.lecturer import Lecturer
from app.models.student_section import StudentSection
from app.models.room import Room
from app.models.time_slot import TimeSlot
from app.models.course_requirement import CourseRequirement
from app.models.lecturer_availability import LecturerAvailability

db = SessionLocal()

try:

    # ==================================================
    # 1. USERS
    # ==================================================

    user1 = db.query(User).filter(
        User.email == "abebe@qinbir.edu.et"
    ).first()

    if not user1:
        user1 = User(
            full_name="Dr. Abebe Kebede",
            email="abebe@qinbir.edu.et",
            password_hash="hashed_password",
            role="LECTURER",
            is_active=True,
        )

        db.add(user1)
        db.commit()
        db.refresh(user1)

    user2 = db.query(User).filter(
        User.email == "hana@qinbir.edu.et"
    ).first()

    if not user2:
        user2 = User(
            full_name="Dr. Hana Tesfaye",
            email="hana@qinbir.edu.et",
            password_hash="hashed_password",
            role="LECTURER",
            is_active=True,
        )

        db.add(user2)
        db.commit()
        db.refresh(user2)

    # ==================================================
    # 2. DEPARTMENT
    # ==================================================

    department = db.query(Department).filter(
        Department.code == "CS"
    ).first()

    if not department:
        department = Department(
            name="Computer Science",
            code="CS",
        )

        db.add(department)
        db.commit()
        db.refresh(department)

    # ==================================================
    # 3. PROGRAM
    # ==================================================

    program = db.query(Program).filter(
        Program.code == "SE"
    ).first()

    if not program:
        program = Program(
            name="Software Engineering",
            code="SE",
            department_id=department.id,
        )

        db.add(program)
        db.commit()
        db.refresh(program)

    # ==================================================
    # 4. COURSES
    # ==================================================

    course1 = db.query(Course).filter(
        Course.code == "SE201"
    ).first()

    if not course1:
        course1 = Course(
            code="SE201",
            name="Database Systems",
            credit_hours=3,
            program_id=program.id,
        )

        db.add(course1)
        db.commit()
        db.refresh(course1)

    course2 = db.query(Course).filter(
        Course.code == "SE202"
    ).first()

    if not course2:
        course2 = Course(
            code="SE202",
            name="Software Engineering",
            credit_hours=3,
            program_id=program.id,
        )

        db.add(course2)
        db.commit()
        db.refresh(course2)

    # ==================================================
    # 5. LECTURERS
    # ==================================================

    lecturer1 = db.query(Lecturer).filter(
        Lecturer.employee_id == "LEC001"
    ).first()

    if not lecturer1:
        lecturer1 = Lecturer(
            user_id=user1.id,
            department_id=department.id,
            employee_id="LEC001",
            name="Dr. Abebe Kebede",
        )

        db.add(lecturer1)
        db.commit()
        db.refresh(lecturer1)

    lecturer2 = db.query(Lecturer).filter(
        Lecturer.employee_id == "LEC002"
    ).first()

    if not lecturer2:
        lecturer2 = Lecturer(
            user_id=user2.id,
            department_id=department.id,
            employee_id="LEC002",
            name="Dr. Hana Tesfaye",
        )

        db.add(lecturer2)
        db.commit()
        db.refresh(lecturer2)

    # ==================================================
    # 6. STUDENT SECTION A
    # ==================================================

    section1 = db.query(StudentSection).filter(
        StudentSection.name == "SE Year 2 Section A"
    ).first()

    if not section1:
        section1 = StudentSection(
            name="SE Year 2 Section A",
            program_id=program.id,
            year=2,
            semester=1,
            student_count=50,
        )

        db.add(section1)
        db.commit()
        db.refresh(section1)

    # ==================================================
    # 7. STUDENT SECTION B
    # ==================================================

    section2 = db.query(StudentSection).filter(
        StudentSection.name == "SE Year 2 Section B"
    ).first()

    if not section2:
        section2 = StudentSection(
            name="SE Year 2 Section B",
            program_id=program.id,
            year=2,
            semester=1,
            student_count=40,
        )

        db.add(section2)
        db.commit()
        db.refresh(section2)

    # ==================================================
    # 8. ROOM 201
    # ==================================================

    room1 = db.query(Room).filter(
        Room.name == "Room 201"
    ).first()

    if not room1:
        room1 = Room(
            name="Room 201",
            building="Main Building",
            capacity=60,
            room_type="CLASSROOM",
        )

        db.add(room1)
        db.commit()
        db.refresh(room1)

    # ==================================================
    # 9. ROOM 202
    # ==================================================

    room2 = db.query(Room).filter(
        Room.name == "Room 202"
    ).first()

    if not room2:
        room2 = Room(
            name="Room 202",
            building="Main Building",
            capacity=80,
            room_type="CLASSROOM",
        )

        db.add(room2)
        db.commit()
        db.refresh(room2)
            # ==================================================
    # ROOM 101 - TOO SMALL FOR BOTH SECTIONS
    # ==================================================

    room3 = db.query(Room).filter(
        Room.name == "Room 101"
    ).first()

    if not room3:
        room3 = Room(
            name="Room 101",
            building="Main Building",
            capacity=30,
            room_type="CLASSROOM",
        )

        db.add(room3)
        db.commit()
        db.refresh(room3)

    # ==================================================
    # 10. TIME SLOTS
    # ==================================================

    time_slot_data = [
    ("Monday", time(8, 0), time(10, 0)),
    ("Monday", time(10, 0), time(12, 0)),
    ("Monday", time(13, 0), time(15, 0)),

    ("Tuesday", time(8, 0), time(10, 0)),
    ("Tuesday", time(10, 0), time(12, 0)),
    ("Tuesday", time(13, 0), time(15, 0)),

    ("Wednesday", time(8, 0), time(10, 0)),
    ("Wednesday", time(10, 0), time(12, 0)),
    ("Wednesday", time(13, 0), time(15, 0)),
]
    time_slots = []

    for day, start_time, end_time in time_slot_data:

        slot = db.query(TimeSlot).filter(
            TimeSlot.day == day,
            TimeSlot.start_time == start_time,
            TimeSlot.end_time == end_time,
        ).first()

        if not slot:

            slot = TimeSlot(
                day=day,
                start_time=start_time,
                end_time=end_time,
            )

            db.add(slot)
            db.commit()
            db.refresh(slot)

        time_slots.append(slot)
        # ==================================================
    # 11. LECTURER AVAILABILITY
    # ==================================================

    monday_8_slot = db.query(TimeSlot).filter(
        TimeSlot.day == "Monday",
        TimeSlot.start_time == time(8, 0),
        TimeSlot.end_time == time(10, 0),
    ).first()

    if monday_8_slot:

        availability = db.query(
            LecturerAvailability
        ).filter(
            LecturerAvailability.lecturer_id == lecturer1.id,
            LecturerAvailability.time_slot_id == monday_8_slot.id,
        ).first()

        if not availability:

            availability = LecturerAvailability(
                lecturer_id=lecturer1.id,
                time_slot_id=monday_8_slot.id,
                is_available=False,
            )

            db.add(availability)
            db.commit()
            db.refresh(availability)
    # ==================================================
    # 11. COURSE REQUIREMENT - SECTION A / SE201
    # ==================================================

    requirement1 = db.query(
        CourseRequirement
    ).filter(
        CourseRequirement.course_id == course1.id,
        CourseRequirement.student_section_id == section1.id,
        CourseRequirement.lecturer_id == lecturer1.id,
    ).first()

    if not requirement1:

        requirement1 = CourseRequirement(
            course_id=course1.id,
            student_section_id=section1.id,
            lecturer_id=lecturer1.id,
            sessions_per_week=3,
        )

        db.add(requirement1)
        db.commit()
        db.refresh(requirement1)

    # ==================================================
    # 12. COURSE REQUIREMENT - SECTION A / SE202
    # ==================================================

    requirement2 = db.query(
        CourseRequirement
    ).filter(
        CourseRequirement.course_id == course2.id,
        CourseRequirement.student_section_id == section1.id,
        CourseRequirement.lecturer_id == lecturer1.id,
    ).first()

    if not requirement2:

        requirement2 = CourseRequirement(
            course_id=course2.id,
            student_section_id=section1.id,
            lecturer_id=lecturer1.id,
            sessions_per_week=3,
        )

        db.add(requirement2)
        db.commit()
        db.refresh(requirement2)

    # ==================================================
    # 13. COURSE REQUIREMENT - SECTION B / SE201
    # ==================================================

    requirement3 = db.query(
        CourseRequirement
    ).filter(
        CourseRequirement.course_id == course1.id,
        CourseRequirement.student_section_id == section2.id,
        CourseRequirement.lecturer_id == lecturer2.id,
    ).first()

    if not requirement3:

        requirement3 = CourseRequirement(
            course_id=course1.id,
            student_section_id=section2.id,
            lecturer_id=lecturer2.id,
            sessions_per_week=3,
        )

        db.add(requirement3)
        db.commit()
        db.refresh(requirement3)

    # ==================================================
    # 14. COURSE REQUIREMENT - SECTION B / SE202
    # ==================================================

    requirement4 = db.query(
        CourseRequirement
    ).filter(
        CourseRequirement.course_id == course2.id,
        CourseRequirement.student_section_id == section2.id,
        CourseRequirement.lecturer_id == lecturer2.id,
    ).first()

    if not requirement4:

        requirement4 = CourseRequirement(
            course_id=course2.id,
            student_section_id=section2.id,
            lecturer_id=lecturer2.id,
            sessions_per_week=3,
        )

        db.add(requirement4)
        db.commit()
        db.refresh(requirement4)

    # ==================================================
    # SUMMARY
    # ==================================================

    print()
    print("QINBIR Test Data")
    print("================")

    print(
        f"Users: "
        f"{db.query(User).count()}"
    )

    print(
        f"Departments: "
        f"{db.query(Department).count()}"
    )

    print(
        f"Programs: "
        f"{db.query(Program).count()}"
    )

    print(
        f"Courses: "
        f"{db.query(Course).count()}"
    )

    print(
        f"Lecturers: "
        f"{db.query(Lecturer).count()}"
    )

    print(
        f"Student sections: "
        f"{db.query(StudentSection).count()}"
    )

    print(
        f"Rooms: "
        f"{db.query(Room).count()}"
    )

    print(
        f"Time slots: "
        f"{db.query(TimeSlot).count()}"
    )

    print(
        f"Course requirements: "
        f"{db.query(CourseRequirement).count()}"
    )

    print()
    print("Test data created/verified successfully!")

except Exception as e:

    db.rollback()

    print()
    print("Error creating test data:")
    print(e)

finally:

    db.close()