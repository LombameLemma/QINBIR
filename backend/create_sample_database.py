import sqlite3
import shutil
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "qinbir.db"

BACKUP_PATH = BASE_DIR / "qinbir_backup_before_50.db"

SAMPLE_SIZE = 50


# ============================================================
# SAMPLE DATA
# ============================================================

departments = [
    ("Computational and Natural Science", "CNS"),
    ("Social Science", "SS"),
    ("Health", "HLT"),
    ("Institute of Technology", "IOT"),
]


programs = [
    ("Computer Science", "CS", 1),
    ("Information Systems", "IS", 1),
    ("Mathematics", "MATH", 1),
    ("Physics", "PHY", 1),
    ("Economics", "ECON", 2),
    ("Management", "MGT", 2),
    ("Psychology", "PSY", 2),
    ("Software Engineering", "SE", 4),
    ("Information Technology", "IT", 4),
    ("Computer Engineering", "CE", 4),
]


course_names = [
    ("Introduction to Programming", 3),
    ("Database Systems", 3),
    ("Data Structures", 3),
    ("Computer Networks", 3),
    ("Operating Systems", 3),
    ("Software Engineering", 3),
    ("Web Development", 3),
    ("Information Systems", 3),
    ("Discrete Mathematics", 2),
    ("Statistics", 2),
]


# ============================================================
# DATABASE BACKUP
# ============================================================

if DB_PATH.exists():
    shutil.copy2(DB_PATH, BACKUP_PATH)
    print()
    print("Current database backed up:")
    print(BACKUP_PATH)
else:
    print("No existing database found.")


# ============================================================
# CONNECT
# ============================================================

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# ============================================================
# DROP TABLES
# ============================================================

tables = [
    "schedule_entries",
    "schedules",
    "constraints",
    "course_requirements",
    "lecturer_availability",
    "program_courses",
    "student_sections",
    "lecturers",
    "users",
    "rooms",
    "time_slots",
    "courses",
    "programs",
    "departments",
]


print()
print("Recreating database...")

for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")


# ============================================================
# CREATE TABLES
# ============================================================

cursor.execute("""
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL
)
""")


cursor.execute("""
CREATE TABLE programs (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
)
""")


cursor.execute("""
CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    credit_hours INTEGER NOT NULL
)
""")


cursor.execute("""
CREATE TABLE program_courses (
    id INTEGER PRIMARY KEY,
    program_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (program_id) REFERENCES programs(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
)
""")


cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME
)
""")


cursor.execute("""
CREATE TABLE lecturers (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (department_id) REFERENCES departments(id)
)
""")


cursor.execute("""
CREATE TABLE student_sections (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    program_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    student_count INTEGER NOT NULL,
    FOREIGN KEY (program_id) REFERENCES programs(id)
)
""")


cursor.execute("""
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    building VARCHAR(100) NOT NULL,
    capacity INTEGER NOT NULL,
    room_type VARCHAR(50) NOT NULL
)
""")


cursor.execute("""
CREATE TABLE time_slots (
    id INTEGER PRIMARY KEY,
    day VARCHAR(20) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
)
""")


cursor.execute("""
CREATE TABLE lecturer_availability (
    id INTEGER PRIMARY KEY,
    lecturer_id INTEGER NOT NULL,
    time_slot_id INTEGER NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(id),
    FOREIGN KEY (time_slot_id) REFERENCES time_slots(id)
)
""")


cursor.execute("""
CREATE TABLE course_requirements (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    student_section_id INTEGER NOT NULL,
    lecturer_id INTEGER NOT NULL,
    sessions_per_week INTEGER NOT NULL DEFAULT 2,
    long_session_hours INTEGER NOT NULL DEFAULT 2,
    short_session_hours INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (student_section_id) REFERENCES student_sections(id),
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(id)
)
""")


cursor.execute("""
CREATE TABLE schedules (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'DRAFT',
    created_at DATETIME,
    approved_at DATETIME,
    published_at DATETIME
)
""")


cursor.execute("""
CREATE TABLE schedule_entries (
    id INTEGER PRIMARY KEY,
    schedule_id INTEGER NOT NULL,
    course_requirement_id INTEGER NOT NULL,
    lecturer_id INTEGER NOT NULL,
    student_section_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    time_slot_id INTEGER NOT NULL,
    FOREIGN KEY (schedule_id) REFERENCES schedules(id),
    FOREIGN KEY (course_requirement_id) REFERENCES course_requirements(id),
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(id),
    FOREIGN KEY (student_section_id) REFERENCES student_sections(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (time_slot_id) REFERENCES time_slots(id)
)
""")


cursor.execute("""
CREATE TABLE constraints (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    weight INTEGER DEFAULT 1
)
""")


# ============================================================
# DEPARTMENTS
# ============================================================

for name, code in departments:
    cursor.execute(
        """
        INSERT INTO departments (name, code)
        VALUES (?, ?)
        """,
        (name, code),
    )


# ============================================================
# PROGRAMS
# ============================================================

for name, code, department_id in programs:
    cursor.execute(
        """
        INSERT INTO programs (name, code, department_id)
        VALUES (?, ?, ?)
        """,
        (name, code, department_id),
    )


# ============================================================
# COURSES
# ============================================================

course_ids = []

for i in range(SAMPLE_SIZE):

    course_name, base_credit = course_names[i % len(course_names)]

    # Mostly 3-credit courses, with some 2-credit courses.
    if i % 10 in (8, 9):
        credit_hours = 2
    else:
        credit_hours = 3

    code = f"CRS{i + 1:03d}"

    cursor.execute(
        """
        INSERT INTO courses
        (code, name, credit_hours)
        VALUES (?, ?, ?)
        """,
        (
            code,
            course_name,
            credit_hours,
        ),
    )

    course_ids.append(cursor.lastrowid)


# ============================================================
# PROGRAM-COURSE RELATIONSHIPS
# ============================================================

program_ids = []

cursor.execute("SELECT id FROM programs ORDER BY id")
program_ids = [row[0] for row in cursor.fetchall()]

for i, course_id in enumerate(course_ids):

    program_id = program_ids[i % len(program_ids)]

    cursor.execute(
        """
        INSERT INTO program_courses
        (program_id, course_id)
        VALUES (?, ?)
        """,
        (
            program_id,
            course_id,
        ),
    )


# ============================================================
# USERS + LECTURERS
# ============================================================

lecturer_ids = []

for i in range(SAMPLE_SIZE):

    full_name = f"Lecturer {i + 1}"
    email = f"lecturer{i + 1}@qinbir.edu.et"
    employee_id = f"EMP{i + 1:03d}"

    department_id = (i % len(departments)) + 1

    cursor.execute(
        """
        INSERT INTO users
        (full_name, email, password_hash, role, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            full_name,
            email,
            "test_password_hash",
            "LECTURER",
            1,
        ),
    )

    user_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO lecturers
        (user_id, department_id, employee_id, name)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            department_id,
            employee_id,
            full_name,
        ),
    )

    lecturer_ids.append(cursor.lastrowid)


# ============================================================
# STUDENT SECTIONS
# ============================================================

section_ids = []

for i in range(SAMPLE_SIZE):

    program_id = program_ids[i % len(program_ids)]

    section_name = f"SECTION-{i + 1:02d}"

    cursor.execute(
        """
        INSERT INTO student_sections
        (name, program_id, year, semester, student_count)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            section_name,
            program_id,
            (i % 4) + 1,
            1,
            40 + (i % 11),
        ),
    )

    section_ids.append(cursor.lastrowid)


# ============================================================
# ROOMS
# ============================================================

for i in range(SAMPLE_SIZE):

    room_number = i + 1

    if i % 3 == 0:
        room_type = "LAB"
        capacity = 50
    elif i % 3 == 1:
        room_type = "CLASSROOM"
        capacity = 60
    else:
        room_type = "CLASSROOM"
        capacity = 80

    cursor.execute(
        """
        INSERT INTO rooms
        (name, building, capacity, room_type)
        VALUES (?, ?, ?, ?)
        """,
        (
            f"Room {room_number}",
            f"Building {(i % 4) + 1}",
            capacity,
            room_type,
        ),
    )


# ============================================================
# TIME SLOTS
# 5 DAYS × 9 SLOTS = 45
# ============================================================

time_slots = [
    ("08:00", "10:00"),
    ("10:00", "12:00"),
    ("13:00", "15:00"),

    ("08:00", "09:00"),
    ("09:00", "10:00"),
    ("10:00", "11:00"),
    ("11:00", "12:00"),
    ("13:00", "14:00"),
    ("14:00", "15:00"),
]

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
]

time_slot_ids = []

for day in days:

    for start_time, end_time in time_slots:

        cursor.execute(
            """
            INSERT INTO time_slots
            (day, start_time, end_time)
            VALUES (?, ?, ?)
            """,
            (
                day,
                start_time,
                end_time,
            ),
        )

        time_slot_ids.append(cursor.lastrowid)


# ============================================================
# LECTURER AVAILABILITY
# 50 LECTURERS × 45 SLOTS = 2250
# ============================================================

availability_count = 0

for lecturer_id in lecturer_ids:

    for time_slot_id in time_slot_ids:

        cursor.execute(
            """
            INSERT INTO lecturer_availability
            (lecturer_id, time_slot_id, is_available)
            VALUES (?, ?, ?)
            """,
            (
                lecturer_id,
                time_slot_id,
                1,
            ),
        )

        availability_count += 1


# ============================================================
# COURSE REQUIREMENTS
# ============================================================

requirement_count = 0

for i in range(SAMPLE_SIZE):

    course_id = course_ids[i]
    lecturer_id = lecturer_ids[i]
    section_id = section_ids[i]

    cursor.execute(
        "SELECT credit_hours FROM courses WHERE id = ?",
        (course_id,),
    )

    credit_hours = cursor.fetchone()[0]

    if credit_hours == 2:

        sessions_per_week = 1
        long_session_hours = 2
        short_session_hours = 0

    else:

        sessions_per_week = 2
        long_session_hours = 2
        short_session_hours = 1

    cursor.execute(
        """
        INSERT INTO course_requirements
        (
            course_id,
            student_section_id,
            lecturer_id,
            sessions_per_week,
            long_session_hours,
            short_session_hours
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            course_id,
            section_id,
            lecturer_id,
            sessions_per_week,
            long_session_hours,
            short_session_hours,
        ),
    )

    requirement_count += 1


# ============================================================
# COMMIT
# ============================================================

conn.commit()


# ============================================================
# VERIFY COUNTS
# ============================================================

def count(table):
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    return cursor.fetchone()[0]


print()
print("=" * 70)
print("50-SAMPLE DATABASE CREATED")
print("=" * 70)

print(f"Departments:       {count('departments')}")
print(f"Programs:          {count('programs')}")
print(f"Courses:           {count('courses')}")
print(f"Users:             {count('users')}")
print(f"Lecturers:         {count('lecturers')}")
print(f"Sections:          {count('student_sections')}")
print(f"Rooms:             {count('rooms')}")
print(f"Time slots:        {count('time_slots')}")
print(f"Availability:      {count('lecturer_availability')}")
print(f"Requirements:      {count('course_requirements')}")

print()
print("Backup:")
print(BACKUP_PATH)

print()
print("Database scaling completed successfully.")

conn.close()