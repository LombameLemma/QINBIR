import sqlite3
import re

DB_PATH = "qinbir.db"


def get_course_year(course_code):
    """
    Determine academic year from the numeric part of a course code.

    Examples:
        CS101  -> Year 1
        CS201  -> Year 2
        CS301  -> Year 3
        CS401  -> Year 4
        MATH101 -> Year 1
    """

    match = re.search(r"(\d{3})$", course_code)

    if not match:
        return None

    number = int(match.group(1))
    year_digit = number // 100

    if year_digit in (1, 2, 3, 4):
        return year_digit

    return None


def main():
    print("=" * 75)
    print("QINBIR COURSE REQUIREMENT SEED")
    print("=" * 75)

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON")

    # ---------------------------------------------------------
    # Load programs
    # ---------------------------------------------------------

    programs = db.execute(
        """
        SELECT id, name, code, department_id
        FROM programs
        ORDER BY id
        """
    ).fetchall()

    print()
    print(f"Programs found:          {len(programs)}")

    # ---------------------------------------------------------
    # Load student sections
    # ---------------------------------------------------------

    sections = db.execute(
        """
        SELECT
            id,
            name,
            program_id,
            year,
            semester,
            student_count
        FROM student_sections
        ORDER BY program_id, year, name
        """
    ).fetchall()

    print(f"Student sections found:  {len(sections)}")

    # ---------------------------------------------------------
    # Load courses
    # ---------------------------------------------------------

    courses = db.execute(
        """
        SELECT id, code, name, credit_hours
        FROM courses
        ORDER BY id
        """
    ).fetchall()

    print(f"Courses found:           {len(courses)}")

    # ---------------------------------------------------------
    # Load program-course relationships
    # ---------------------------------------------------------

    relationships = db.execute(
        """
        SELECT program_id, course_id
        FROM program_courses
        ORDER BY program_id, course_id
        """
    ).fetchall()

    print(f"Program-course links:    {len(relationships)}")

    # ---------------------------------------------------------
    # Load lecturers
    #
    # Lecturers belong to departments in the current model.
    # We therefore use lecturers from the same department.
    # ---------------------------------------------------------

    lecturers = db.execute(
        """
        SELECT
            id,
            name,
            department_id,
            employee_id
        FROM lecturers
        ORDER BY department_id, id
        """
    ).fetchall()

    print(f"Lecturers found:         {len(lecturers)}")

    if not programs:
        print("ERROR: No programs found.")
        db.close()
        return

    if not sections:
        print("ERROR: No student sections found.")
        db.close()
        return

    if not courses:
        print("ERROR: No courses found.")
        db.close()
        return

    if not relationships:
        print("ERROR: No program-course relationships found.")
        db.close()
        return

    if not lecturers:
        print("ERROR: No lecturers found.")
        db.close()
        return

    # ---------------------------------------------------------
    # Convert data to dictionaries
    # ---------------------------------------------------------

    program_map = {}

    for program_id, name, code, department_id in programs:
        program_map[program_id] = {
            "name": name,
            "code": code,
            "department_id": department_id,
        }

    course_map = {}

    for course_id, code, name, credit_hours in courses:
        course_map[course_id] = {
            "code": code,
            "name": name,
            "credit_hours": credit_hours,
        }

    # ---------------------------------------------------------
    # Group sections by program and year
    # ---------------------------------------------------------

    section_map = {}

    for (
        section_id,
        section_name,
        program_id,
        year,
        semester,
        student_count,
    ) in sections:

        key = (program_id, year, semester)

        section_map.setdefault(key, []).append(
            {
                "id": section_id,
                "name": section_name,
                "student_count": student_count,
            }
        )

    # ---------------------------------------------------------
    # Group lecturers by department
    # ---------------------------------------------------------

    department_lecturers = {}

    for lecturer_id, name, department_id, employee_id in lecturers:

        department_lecturers.setdefault(
            department_id,
            []
        ).append(
            {
                "id": lecturer_id,
                "name": name,
                "employee_id": employee_id,
            }
        )

    # ---------------------------------------------------------
    # Group courses by program
    # ---------------------------------------------------------

    program_courses = {}

    for program_id, course_id in relationships:

        program_courses.setdefault(
            program_id,
            []
        ).append(course_id)

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    created = 0
    existing = 0
    skipped = 0

    print()
    print("Creating course requirements...")
    print("-" * 75)

    # ---------------------------------------------------------
    # Process every program
    # ---------------------------------------------------------

    for program_id, program in program_map.items():

        program_code = program["code"]
        program_name = program["name"]
        department_id = program["department_id"]

        lecturer_list = department_lecturers.get(
            department_id,
            []
        )

        if not lecturer_list:
            print(
                f"WARNING: No lecturers for department "
                f"of {program_code}"
            )
            continue

        course_ids = program_courses.get(
            program_id,
            []
        )

        program_created = 0

        print(
            f"{program_code:<8} "
            f"{program_name:<50}"
        )

        # -----------------------------------------------------
        # Process courses connected to this program
        # -----------------------------------------------------

        for course_id in course_ids:

            course = course_map.get(course_id)

            if not course:
                continue

            course_code = course["code"]
            course_name = course["name"]

            course_year = get_course_year(
                course_code
            )

            # -------------------------------------------------
            # If we cannot determine year, skip it.
            # This prevents incorrect scheduling assignments.
            # -------------------------------------------------

            if course_year is None:
                skipped += 1

                print(
                    f"  SKIP {course_code:<12} "
                    f"Cannot determine academic year"
                )

                continue

            # -------------------------------------------------
            # Find sections in the same program/year.
            # Semester 1 is what we seeded.
            # -------------------------------------------------

            matching_sections = section_map.get(
                (
                    program_id,
                    course_year,
                    1,
                ),
                []
            )

            if not matching_sections:
                skipped += 1
                continue

            # -------------------------------------------------
            # Choose lecturer deterministically.
            #
            # Each program's courses are distributed among
            # lecturers in its department.
            # -------------------------------------------------

            lecturer_index = (
                course_id % len(lecturer_list)
            )

            selected_lecturer = lecturer_list[
                lecturer_index
            ]

            lecturer_id = selected_lecturer["id"]

            # -------------------------------------------------
            # Create one requirement for every section.
            # -------------------------------------------------

            for section in matching_sections:

                section_id = section["id"]

                # ---------------------------------------------
                # Check for duplicate
                # ---------------------------------------------

                existing_requirement = db.execute(
                    """
                    SELECT id
                    FROM course_requirements
                    WHERE course_id = ?
                      AND student_section_id = ?
                    """,
                    (
                        course_id,
                        section_id,
                    )
                ).fetchone()

                if existing_requirement:
                    existing += 1
                    continue

                # ---------------------------------------------
                # Create requirement
                #
                # 2 sessions per week:
                #   one 2-hour session
                #   one 1-hour session
                # ---------------------------------------------

                db.execute(
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
                        2,
                        2,
                        1,
                    )
                )

                created += 1
                program_created += 1

        print(
            f"         Requirements created: "
            f"{program_created}"
        )

    db.commit()

    # ---------------------------------------------------------
    # Final statistics
    # ---------------------------------------------------------

    total_requirements = db.execute(
        """
        SELECT COUNT(*)
        FROM course_requirements
        """
    ).fetchone()[0]

    print()
    print("=" * 75)
    print("COURSE REQUIREMENT SEED COMPLETE")
    print("=" * 75)

    print(f"Requirements created:    {created}")
    print(f"Already existed:         {existing}")
    print(f"Skipped:                 {skipped}")
    print(f"Total requirements:      {total_requirements}")

    # ---------------------------------------------------------
    # Verification summary
    # ---------------------------------------------------------

    print()
    print("REQUIREMENTS BY DEPARTMENT")
    print("-" * 75)

    department_summary = db.execute(
        """
        SELECT
            d.code,
            d.name,
            COUNT(cr.id)
        FROM departments d
        LEFT JOIN programs p
            ON p.department_id = d.id
        LEFT JOIN student_sections ss
            ON ss.program_id = p.id
        LEFT JOIN course_requirements cr
            ON cr.student_section_id = ss.id
        GROUP BY d.id
        ORDER BY d.id
        """
    ).fetchall()

    for code, name, count in department_summary:
        print(
            f"{code:<8} "
            f"{name:<45} "
            f"{count:>6} requirements"
        )

    # ---------------------------------------------------------
    # Requirements by program
    # ---------------------------------------------------------

    print()
    print("REQUIREMENTS BY PROGRAM")
    print("-" * 75)

    program_summary = db.execute(
        """
        SELECT
            p.code,
            p.name,
            COUNT(cr.id)
        FROM programs p
        LEFT JOIN student_sections ss
            ON ss.program_id = p.id
        LEFT JOIN course_requirements cr
            ON cr.student_section_id = ss.id
        GROUP BY p.id
        ORDER BY p.id
        """
    ).fetchall()

    for code, name, count in program_summary:
        print(
            f"{code:<8} "
            f"{name:<50} "
            f"{count:>5}"
        )

    db.close()

    print()
    print("Database connection closed.")
    print("QINBIR course requirements are ready.")


if __name__ == "__main__":
    main()