import sqlite3
from pathlib import Path


# ============================================================
# DATABASE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

SOURCE_DB = BASE_DIR / "qinbir.db"
TEST_DB = BASE_DIR / "qinbir_test.db"


# ============================================================
# REMOVE OLD TEST DATABASE
# ============================================================

if TEST_DB.exists():
    TEST_DB.unlink()


# ============================================================
# CONNECT
# ============================================================

source = sqlite3.connect(SOURCE_DB)
test = sqlite3.connect(TEST_DB)

source.row_factory = sqlite3.Row
test.row_factory = sqlite3.Row


# ============================================================
# CREATE TABLE STRUCTURE
# ============================================================

schema = """
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE programs (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    department_id INTEGER NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(150) NOT NULL,
    hashed_password VARCHAR(255),
    role VARCHAR(30)
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    credit_hours INTEGER NOT NULL
);

CREATE TABLE program_courses (
    id INTEGER PRIMARY KEY,
    program_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL
);

CREATE TABLE lecturers (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    employee_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE student_sections (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    program_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    student_count INTEGER NOT NULL
);

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    building VARCHAR(100) NOT NULL,
    capacity INTEGER NOT NULL,
    room_type VARCHAR(50) NOT NULL
);

CREATE TABLE time_slots (
    id INTEGER PRIMARY KEY,
    day VARCHAR(20) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

CREATE TABLE lecturer_availability (
    id INTEGER PRIMARY KEY,
    lecturer_id INTEGER NOT NULL,
    time_slot_id INTEGER NOT NULL,
    is_available BOOLEAN NOT NULL
);

CREATE TABLE course_requirements (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    student_section_id INTEGER NOT NULL,
    lecturer_id INTEGER NOT NULL,
    sessions_per_week INTEGER NOT NULL,
    long_session_hours INTEGER NOT NULL,
    short_session_hours INTEGER NOT NULL
);

CREATE TABLE schedules (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at DATETIME NOT NULL,
    approved_at DATETIME,
    published_at DATETIME
);

CREATE TABLE schedule_entries (
    id INTEGER PRIMARY KEY,
    schedule_id INTEGER NOT NULL,
    course_requirement_id INTEGER NOT NULL,
    lecturer_id INTEGER NOT NULL,
    student_section_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    time_slot_id INTEGER NOT NULL
);

CREATE TABLE constraints (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL,
    weight INTEGER NOT NULL
);
"""

test.executescript(schema)


# ============================================================
# HELPER
# ============================================================

def copy_rows(table, columns, limit=None):
    query = f"SELECT {', '.join(columns)} FROM {table}"

    if limit:
        query += f" LIMIT {limit}"

    rows = source.execute(query).fetchall()

    placeholders = ",".join(["?"] * len(columns))

    test.executemany(
        f"""
        INSERT INTO {table} ({', '.join(columns)})
        VALUES ({placeholders})
        """,
        [tuple(row[column] for column in columns) for row in rows]
    )

    return rows


# ============================================================
# DEPARTMENTS
# ============================================================

departments = source.execute("""
    SELECT *
    FROM departments
    ORDER BY id
    LIMIT 2
""").fetchall()

test.executemany(
    """
    INSERT INTO departments (id, name, code)
    VALUES (?, ?, ?)
    """,
    [
        (
            row["id"],
            row["name"],
            row["code"]
        )
        for row in departments
    ]
)


department_ids = [row["id"] for row in departments]


# ============================================================
# PROGRAMS
# ============================================================

programs = source.execute("""
    SELECT *
    FROM programs
    WHERE department_id IN ({})
    ORDER BY id
    LIMIT 4
""".format(",".join("?" * len(department_ids))), department_ids).fetchall()

test.executemany(
    """
    INSERT INTO programs (
        id,
        name,
        code,
        department_id
    )
    VALUES (?, ?, ?, ?)
    """,
    [
        (
            row["id"],
            row["name"],
            row["code"],
            row["department_id"]
        )
        for row in programs
    ]
)

program_ids = [row["id"] for row in programs]


# ============================================================
# COURSES
# ============================================================

courses = source.execute("""
    SELECT *
    FROM courses
    WHERE credit_hours = 3
    ORDER BY id
    LIMIT 10
""").fetchall()

test.executemany(
    """
    INSERT INTO courses (
        id,
        code,
        name,
        credit_hours
    )
    VALUES (?, ?, ?, ?)
    """,
    [
        (
            row["id"],
            row["code"],
            row["name"],
            row["credit_hours"]
        )
        for row in courses
    ]
)

course_ids = [row["id"] for row in courses]


# ============================================================
# PROGRAM-COURSE RELATIONSHIPS
# ============================================================

if course_ids and program_ids:

    placeholders_courses = ",".join("?" * len(course_ids))
    placeholders_programs = ",".join("?" * len(program_ids))

    relationships = source.execute(
        f"""
        SELECT *
        FROM program_courses
        WHERE course_id IN ({placeholders_courses})
          AND program_id IN ({placeholders_programs})
        """,
        course_ids + program_ids
    ).fetchall()

    test.executemany(
        """
        INSERT INTO program_courses (
            id,
            program_id,
            course_id
        )
        VALUES (?, ?, ?)
        """,
        [
            (
                row["id"],
                row["program_id"],
                row["course_id"]
            )
            for row in relationships
        ]
    )


# ============================================================
# USERS
# ============================================================

users = source.execute("""
    SELECT *
    FROM users
    ORDER BY id
    LIMIT 10
""").fetchall()

user_columns = [
    "id",
    "email",
    "hashed_password",
    "role"
]

test.executemany(
    """
    INSERT INTO users (
        id,
        email,
        hashed_password,
        role
    )
    VALUES (?, ?, ?, ?)
    """,
    [
        tuple(row[column] for column in user_columns)
        for row in users
    ]
)

user_ids = [row["id"] for row in users]


# ============================================================
# LECTURERS
# ============================================================

lecturers = source.execute("""
    SELECT *
    FROM lecturers
    WHERE user_id IN ({})
    ORDER BY id
    LIMIT 10
""".format(",".join("?" * len(user_ids))), user_ids).fetchall()

test.executemany(
    """
    INSERT INTO lecturers (
        id,
        user_id,
        department_id,
        employee_id,
        name
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    [
        (
            row["id"],
            row["user_id"],
            row["department_id"],
            row["employee_id"],
            row["name"]
        )
        for row in lecturers
    ]
)

lecturer_ids = [row["id"] for row in lecturers]


# ============================================================
# STUDENT SECTIONS
# ============================================================

sections = source.execute("""
    SELECT *
    FROM student_sections
    WHERE program_id IN ({})
    ORDER BY id
    LIMIT 10
""".format(",".join("?" * len(program_ids))), program_ids).fetchall()

test.executemany(
    """
    INSERT INTO student_sections (
        id,
        name,
        program_id,
        year,
        semester,
        student_count
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    [
        (
            row["id"],
            row["name"],
            row["program_id"],
            row["year"],
            row["semester"],
            row["student_count"]
        )
        for row in sections
    ]
)

section_ids = [row["id"] for row in sections]


# ============================================================
# ROOMS
# ============================================================

rooms = source.execute("""
    SELECT *
    FROM rooms
    WHERE capacity >= 60
    ORDER BY capacity, id
    LIMIT 10
""").fetchall()

test.executemany(
    """
    INSERT INTO rooms (
        id,
        name,
        building,
        capacity,
        room_type
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    [
        (
            row["id"],
            row["name"],
            row["building"],
            row["capacity"],
            row["room_type"]
        )
        for row in rooms
    ]
)


# ============================================================
# TIME SLOTS
# ============================================================

time_slots = source.execute("""
    SELECT *
    FROM time_slots
    ORDER BY id
""").fetchall()

test.executemany(
    """
    INSERT INTO time_slots (
        id,
        day,
        start_time,
        end_time
    )
    VALUES (?, ?, ?, ?)
    """,
    [
        (
            row["id"],
            row["day"],
            row["start_time"],
            row["end_time"]
        )
        for row in time_slots
    ]
)

time_slot_ids = [row["id"] for row in time_slots]


# ============================================================
# LECTURER AVAILABILITY
# ============================================================

availability = source.execute(
    f"""
    SELECT *
    FROM lecturer_availability
    WHERE lecturer_id IN ({",".join("?" * len(lecturer_ids))})
    AND time_slot_id IN ({",".join("?" * len(time_slot_ids))})
    """,
    lecturer_ids + time_slot_ids
).fetchall()

test.executemany(
    """
    INSERT INTO lecturer_availability (
        id,
        lecturer_id,
        time_slot_id,
        is_available
    )
    VALUES (?, ?, ?, ?)
    """,
    [
        (
            row["id"],
            row["lecturer_id"],
            row["time_slot_id"],
            row["is_available"]
        )
        for row in availability
    ]
)


# ============================================================
# COURSE REQUIREMENTS
# ============================================================

requirements = source.execute(
    f"""
    SELECT *
    FROM course_requirements
    WHERE course_id IN ({",".join("?" * len(course_ids))})
      AND student_section_id IN ({",".join("?" * len(section_ids))})
      AND lecturer_id IN ({",".join("?" * len(lecturer_ids))})
    ORDER BY id
    LIMIT 15
    """,
    course_ids + section_ids + lecturer_ids
).fetchall()

test.executemany(
    """
    INSERT INTO course_requirements (
        id,
        course_id,
        student_section_id,
        lecturer_id,
        sessions_per_week,
        long_session_hours,
        short_session_hours
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    [
        (
            row["id"],
            row["course_id"],
            row["student_section_id"],
            row["lecturer_id"],
            row["sessions_per_week"],
            row["long_session_hours"],
            row["short_session_hours"]
        )
        for row in requirements
    ]
)


# ============================================================
# CONSTRAINTS
# ============================================================

constraints = source.execute("""
    SELECT *
    FROM constraints
    ORDER BY id
    LIMIT 20
""").fetchall()

test.executemany(
    """
    INSERT INTO constraints (
        id,
        name,
        type,
        description,
        is_active,
        weight
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    [
        (
            row["id"],
            row["name"],
            row["type"],
            row["description"],
            row["is_active"],
            row["weight"]
        )
        for row in constraints
    ]
)


# ============================================================
# COMMIT
# ============================================================

test.commit()

source.close()
test.close()


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 70)
print("QINBIR TEST DATABASE CREATED")
print("=" * 70)
print()

conn = sqlite3.connect(TEST_DB)

tables = [
    "departments",
    "programs",
    "courses",
    "program_courses",
    "users",
    "lecturers",
    "student_sections",
    "rooms",
    "time_slots",
    "lecturer_availability",
    "course_requirements",
    "constraints",
]

for table in tables:
    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(
        f"{table:<30} {count:>5}"
    )

conn.close()

print()
print(f"Test database:")
print(TEST_DB)
print()