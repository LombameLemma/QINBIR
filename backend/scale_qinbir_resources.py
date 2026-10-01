import sqlite3
from collections import defaultdict

DB_PATH = "qinbir.db"

TARGET_ROOMS = 110
EXTRA_LECTURERS_PER_DEPARTMENT = 5


def main():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row

    print("=" * 70)
    print("QINBIR RESOURCE SCALING")
    print("=" * 70)

    # ============================================================
    # Current counts
    # ============================================================

    current_rooms = db.execute(
        "SELECT COUNT(*) AS count FROM rooms"
    ).fetchone()["count"]

    current_lecturers = db.execute(
        "SELECT COUNT(*) AS count FROM lecturers"
    ).fetchone()["count"]

    current_users = db.execute(
        "SELECT COUNT(*) AS count FROM users"
    ).fetchone()["count"]

    print()
    print("CURRENT RESOURCES")
    print("-" * 70)
    print(f"Rooms:       {current_rooms}")
    print(f"Lecturers:   {current_lecturers}")
    print(f"Users:       {current_users}")

    # ============================================================
    # 1. Add rooms
    # ============================================================

    rooms_needed = max(
        0,
        TARGET_ROOMS - current_rooms
    )

    print()
    print("ROOM SCALING")
    print("-" * 70)
    print(f"Target rooms: {TARGET_ROOMS}")
    print(f"Rooms to add: {rooms_needed}")

    capacities = [
        30,
        30,
        35,
        35,
        40,
        40,
        45,
        45,
        50,
        50,
        55,
        60,
        60,
        70,
        80,
    ]

    buildings = [
        "Main Building",
        "Science Building",
        "Technology Building",
        "Engineering Building",
        "Health Sciences Building",
    ]

    next_room_number = current_rooms + 1

    for index in range(rooms_needed):

        room_number = next_room_number + index

        building = buildings[
            index % len(buildings)
        ]

        capacity = capacities[
            index % len(capacities)
        ]

        room_name = f"Room {room_number:03d}"

        db.execute(
            """
            INSERT INTO rooms
            (
                name,
                building,
                capacity,
                room_type
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                room_name,
                building,
                capacity,
                "CLASSROOM",
            ),
        )

    # ============================================================
    # 2. Add lecturers
    # ============================================================

    departments = db.execute(
        """
        SELECT
            id,
            code,
            name
        FROM departments
        ORDER BY id
        """
    ).fetchall()

    print()
    print("LECTURER SCALING")
    print("-" * 70)

    next_lecturer_number = (
        current_lecturers + 1
    )

    lecturer_number = next_lecturer_number

    for department in departments:

        existing_count = db.execute(
            """
            SELECT COUNT(*) AS count
            FROM lecturers
            WHERE department_id = ?
            """,
            (department["id"],),
        ).fetchone()["count"]

        print(
            f"{department['code']}: "
            f"{existing_count} existing + "
            f"{EXTRA_LECTURERS_PER_DEPARTMENT} new"
        )

        for number in range(
            EXTRA_LECTURERS_PER_DEPARTMENT
        ):

            employee_id = (
                f"LEC{lecturer_number:03d}"
            )

            email = (
                f"lecturer{lecturer_number}"
                "@qinbir.edu.et"
            )

            name = (
                f"Lecturer "
                f"{lecturer_number}"
            )

            # ----------------------------------------------------
            # Create user
            # ----------------------------------------------------

            cursor = db.execute(
                """
                INSERT INTO users
                (
                    full_name,
                    email,
                    password_hash,
                    role,
                    is_active
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    "seed_password",
                    "LECTURER",
                    1,
                ),
            )

            user_id = cursor.lastrowid

            # ----------------------------------------------------
            # Create lecturer
            # ----------------------------------------------------

            db.execute(
                """
                INSERT INTO lecturers
                (
                    user_id,
                    department_id,
                    employee_id,
                    name
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    user_id,
                    department["id"],
                    employee_id,
                    name,
                ),
            )

            lecturer_number += 1

    db.commit()

    # ============================================================
    # 3. Rebalance course requirements
    # ============================================================

    print()
    print("REBALANCING COURSE REQUIREMENTS")
    print("-" * 70)

    # ------------------------------------------------------------
    # Build department → lecturer list
    # ------------------------------------------------------------

    lecturers_by_department = defaultdict(list)

    lecturer_rows = db.execute(
        """
        SELECT
            l.id,
            l.department_id
        FROM lecturers l
        ORDER BY l.department_id, l.id
        """
    ).fetchall()

    for lecturer in lecturer_rows:

        lecturers_by_department[
            lecturer["department_id"]
        ].append(
            lecturer["id"]
        )

    # ------------------------------------------------------------
    # Requirements joined to program department
    # ------------------------------------------------------------

    requirements = db.execute(
        """
        SELECT
            cr.id AS requirement_id,
            p.department_id
        FROM course_requirements cr

        JOIN student_sections ss
            ON ss.id = cr.student_section_id

        JOIN programs p
            ON p.id = ss.program_id

        ORDER BY
            p.department_id,
            cr.id
        """
    ).fetchall()

    # ------------------------------------------------------------
    # Round-robin requirements across department lecturers
    # ------------------------------------------------------------

    department_positions = defaultdict(int)

    changed = 0

    for requirement in requirements:

        department_id = requirement[
            "department_id"
        ]

        lecturer_list = lecturers_by_department[
            department_id
        ]

        if not lecturer_list:
            print(
                f"WARNING: No lecturers for "
                f"department {department_id}"
            )
            continue

        position = department_positions[
            department_id
        ]

        lecturer_id = lecturer_list[
            position % len(lecturer_list)
        ]

        department_positions[
            department_id
        ] = position + 1

        db.execute(
            """
            UPDATE course_requirements
            SET lecturer_id = ?
            WHERE id = ?
            """,
            (
                lecturer_id,
                requirement["requirement_id"],
            ),
        )

        changed += 1

    db.commit()

    # ============================================================
    # 4. Final statistics
    # ============================================================

    final_rooms = db.execute(
        "SELECT COUNT(*) AS count FROM rooms"
    ).fetchone()["count"]

    final_lecturers = db.execute(
        "SELECT COUNT(*) AS count FROM lecturers"
    ).fetchone()["count"]

    final_users = db.execute(
        "SELECT COUNT(*) AS count FROM users"
    ).fetchone()["count"]

    requirements_count = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM course_requirements
        """
    ).fetchone()["count"]

    # ============================================================
    # Lecturer workload calculation
    # ============================================================

    workload_rows = db.execute(
        """
        SELECT
            l.id,
            l.name,
            d.code AS department_code,
            COUNT(cr.id) AS requirements_count
        FROM lecturers l

        JOIN departments d
            ON d.id = l.department_id

        LEFT JOIN course_requirements cr
            ON cr.lecturer_id = l.id

        GROUP BY
            l.id,
            l.name,
            d.code

        ORDER BY
            d.code,
            requirements_count DESC
        """
    ).fetchall()

    print()
    print("=" * 70)
    print("RESOURCE SCALING COMPLETE")
    print("=" * 70)

    print()
    print("FINAL RESOURCES")
    print("-" * 70)

    print(
        f"Rooms:              {final_rooms}"
    )

    print(
        f"Lecturers:          {final_lecturers}"
    )

    print(
        f"Users:              {final_users}"
    )

    print(
        f"Course requirements: {requirements_count}"
    )

    print()
    print("THEORETICAL WEEKLY CAPACITY")
    print("-" * 70)

    print(
        f"Room capacity: "
        f"{final_rooms} × 30 = "
        f"{final_rooms * 30:,} room-hours"
    )

    print(
        f"Lecturer capacity: "
        f"{final_lecturers} × 30 = "
        f"{final_lecturers * 30:,} lecturer-hours"
    )

    required_hours = requirements_count * 3

    print(
        f"Required teaching: "
        f"{requirements_count} × 3 = "
        f"{required_hours:,} hours"
    )

    print()
    print("LECTURER WORKLOAD")
    print("-" * 70)

    current_department = None

    for row in workload_rows:

        if row["department_code"] != current_department:

            current_department = (
                row["department_code"]
            )

            print()
            print(
                f"[{current_department}]"
            )

        print(
            f"{row['name']:<22} "
            f"{row['requirements_count']:>3} "
            f"requirements = "
            f"{row['requirements_count'] * 3:>3} hours"
        )

    db.close()

    print()
    print("Database connection closed.")


if __name__ == "__main__":
    main()