from sqlalchemy import text

from app.database import engine


with engine.begin() as connection:

    # Add the new columns if they do not already exist
    connection.execute(text("""
        ALTER TABLE course_requirements
        ADD COLUMN long_session_hours INTEGER NOT NULL DEFAULT 2
    """))

    connection.execute(text("""
        ALTER TABLE course_requirements
        ADD COLUMN short_session_hours INTEGER NOT NULL DEFAULT 1
    """))

    # Change 3 weekly sessions into 2 meetings:
    # one 2-hour class + one 1-hour class
    connection.execute(text("""
        UPDATE course_requirements
        SET sessions_per_week = 2,
            long_session_hours = 2,
            short_session_hours = 1
    """))


print()
print("QINBIR Course Requirement Update")
print("=================================")
print("Course requirements updated successfully.")
print("Each requirement now has:")
print("  - 2 sessions per week")
print("  - 1 session of 2 hours")
print("  - 1 session of 1 hour")