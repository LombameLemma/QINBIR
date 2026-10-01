import sqlite3
import shutil
from pathlib import Path


DB_PATH = Path("qinbir.db")
BACKUP_PATH = Path("qinbir_backup_before_course_migration.db")


# ---------------------------------------------------------
# Safety check
# ---------------------------------------------------------

if not DB_PATH.exists():
    raise FileNotFoundError("qinbir.db was not found.")


# ---------------------------------------------------------
# Create backup if it does not already exist
# ---------------------------------------------------------

if not BACKUP_PATH.exists():

    shutil.copy2(
        DB_PATH,
        BACKUP_PATH
    )

    print("Backup created:")
    print(BACKUP_PATH.resolve())

else:

    print("Backup already exists:")
    print(BACKUP_PATH.resolve())


# ---------------------------------------------------------
# Connect to database
# ---------------------------------------------------------

db = sqlite3.connect(DB_PATH)

try:

    # -----------------------------------------------------
    # Check current courses table
    # -----------------------------------------------------

    columns = db.execute(
        "PRAGMA table_info(courses)"
    ).fetchall()

    print("\nCurrent courses table:")

    for column in columns:
        print(column)


    column_names = [
        column[1]
        for column in columns
    ]


    # -----------------------------------------------------
    # Check whether migration is already complete
    # -----------------------------------------------------

    if "program_id" not in column_names:

        print(
            "\nprogram_id is already removed."
        )

        db.close()

        raise SystemExit


    # -----------------------------------------------------
    # Count existing relationships
    # -----------------------------------------------------

    relationship_count = db.execute(
        "SELECT COUNT(*) FROM program_courses"
    ).fetchone()[0]

    print(
        f"\nProgram-course relationships found: "
        f"{relationship_count}"
    )


    # -----------------------------------------------------
    # Begin transaction
    # -----------------------------------------------------

    db.execute("BEGIN")


    # -----------------------------------------------------
    # Create new courses table
    # -----------------------------------------------------

    db.execute(
        """
        CREATE TABLE courses_new (
            id INTEGER NOT NULL PRIMARY KEY,
            code VARCHAR(20) NOT NULL,
            name VARCHAR(150) NOT NULL,
            credit_hours INTEGER NOT NULL
        )
        """
    )


    # -----------------------------------------------------
    # Copy existing courses
    # -----------------------------------------------------

    db.execute(
        """
        INSERT INTO courses_new (
            id,
            code,
            name,
            credit_hours
        )
        SELECT
            id,
            code,
            name,
            credit_hours
        FROM courses
        """
    )


    # -----------------------------------------------------
    # Delete old courses table
    # -----------------------------------------------------

    db.execute(
        "DROP TABLE courses"
    )


    # -----------------------------------------------------
    # Rename new table
    # -----------------------------------------------------

    db.execute(
        "ALTER TABLE courses_new RENAME TO courses"
    )


    # -----------------------------------------------------
    # Recreate indexes
    # -----------------------------------------------------

    db.execute(
        """
        CREATE INDEX ix_courses_id
        ON courses(id)
        """
    )

    db.execute(
        """
        CREATE UNIQUE INDEX ix_courses_code
        ON courses(code)
        """
    )


    # -----------------------------------------------------
    # Commit migration
    # -----------------------------------------------------

    db.commit()


    print(
        "\nMigration completed successfully."
    )


    # -----------------------------------------------------
    # Verify new courses table
    # -----------------------------------------------------

    columns = db.execute(
        "PRAGMA table_info(courses)"
    ).fetchall()

    print(
        "\nNew courses table:"
    )

    for column in columns:
        print(column)


    # -----------------------------------------------------
    # Verify course count
    # -----------------------------------------------------

    course_count = db.execute(
        "SELECT COUNT(*) FROM courses"
    ).fetchone()[0]

    print(
        f"\nCourses preserved: "
        f"{course_count}"
    )


    # -----------------------------------------------------
    # Verify program-course relationships
    # -----------------------------------------------------

    relationship_count = db.execute(
        "SELECT COUNT(*) FROM program_courses"
    ).fetchone()[0]

    print(
        f"Program-course relationships preserved: "
        f"{relationship_count}"
    )


except Exception:

    db.rollback()

    print(
        "\nMigration failed."
    )

    print(
        "Database transaction was rolled back."
    )

    raise


finally:

    db.close()