
import sqlite3
from pathlib import Path

ACTIVE_DB = Path("qinbir.db")
BACKUP_DB = Path("qinbir_backup_before_recovery.db")

def restore():
    if not ACTIVE_DB.exists() or not BACKUP_DB.exists():
        raise FileNotFoundError("Active or backup database not found.")

    db = sqlite3.connect(ACTIVE_DB)
    backup = sqlite3.connect(BACKUP_DB)

    try:
        db.execute("PRAGMA foreign_keys = ON")

        # Read source records without modifying the backup.
        accounts = backup.execute("""
            SELECT id, full_name, email, password_hash,
                   role, is_active, created_at
            FROM users
            WHERE id IN (51, 52)
            ORDER BY id
        """).fetchall()

        student = backup.execute("""
            SELECT id, user_id, student_id, program_id
            FROM students
            WHERE user_id = 52
        """).fetchone()

        if len(accounts) != 2 or student is None:
            raise RuntimeError("Expected backup records are missing.")

        if {row[4] for row in accounts} != {"ADMIN", "STUDENT"}:
            raise RuntimeError("Unexpected account roles in backup.")

        # Confirm no conflicting records.
        for account in accounts:
            user_id, _, email = account[:3]

            if db.execute(
                "SELECT 1 FROM users WHERE id = ? OR lower(email) = lower(?)",
                (user_id, email)
            ).fetchone():
                raise RuntimeError(f"User ID or email already exists: {email}")

        if db.execute(
            "SELECT 1 FROM students WHERE id = ? OR student_id = ?",
            (student[0], student[2])
        ).fetchone():
            raise RuntimeError("Student profile ID or student ID already exists.")

        # Confirm referenced program exists.
        if not db.execute(
            "SELECT 1 FROM programs WHERE id = ?",
            (student[3],)
        ).fetchone():
            raise RuntimeError("Student program does not exist in active DB.")

        # Begin an atomic transaction.
        db.execute("BEGIN IMMEDIATE")

        db.executemany("""
            INSERT INTO users
            (id, full_name, email, password_hash, role, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, accounts)

        # Active schema has no section_id column.
        db.execute("""
            INSERT INTO students (id, user_id, student_id, program_id)
            VALUES (?, ?, ?, ?)
        """, student)

        db.commit()

        print("RESTORATION SUCCESSFUL")
        print("Admin account restored.")
        print("Student account restored.")
        print("Student profile restored.")
        print("Original password hashes preserved.")

    except Exception:
        db.rollback()
        raise

    finally:
        backup.close()
        db.close()


if __name__ == "__main__":
    restore()
