# Load the complete SQLAlchemy model metadata first.
from app.main import app

from sqlalchemy import text

from app.database import SessionLocal
from app.models.program_course import ProgramCourse


db = SessionLocal()

try:
    # Read the old Course -> Program relationships
    # directly from the existing SQLite database.
    rows = db.execute(
        text(
            """
            SELECT id, program_id
            FROM courses
            WHERE program_id IS NOT NULL
            """
        )
    ).fetchall()

    print(f"Old relationships found: {len(rows)}")

    migrated = 0

    for course_id, program_id in rows:

        existing = (
            db.query(ProgramCourse)
            .filter(
                ProgramCourse.program_id == program_id,
                ProgramCourse.course_id == course_id
            )
            .first()
        )

        if existing:
            continue

        relationship = ProgramCourse(
            program_id=program_id,
            course_id=course_id
        )

        db.add(relationship)
        migrated += 1

    db.commit()

    print(f"Migrated relationships: {migrated}")

    print("\nProgram-Course relationships:")

    relationships = (
        db.query(ProgramCourse)
        .order_by(ProgramCourse.id)
        .all()
    )

    for relationship in relationships:
        print(
            f"Program ID {relationship.program_id} "
            f"<-> Course ID {relationship.course_id}"
        )

except Exception:
    db.rollback()
    raise

finally:
    db.close()