
import getpass

from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password

STUDENT_EMAIL = "studenttest1@qinbir.edu.et"

db = SessionLocal()

try:
    student = db.query(User).filter(
        User.email == STUDENT_EMAIL
    ).first()

    if student is None or student.role.upper() != "STUDENT":
        raise RuntimeError("Student account not found.")

    password = getpass.getpass("Enter new student password: ")
    confirmation = getpass.getpass("Confirm new student password: ")

    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    if password != confirmation:
        raise ValueError("Passwords do not match.")

    student.password_hash = hash_password(password)
    db.commit()

    print("SUCCESS: Student password updated.")
    print("Account:", STUDENT_EMAIL)

except Exception as error:
    db.rollback()
    print("ERROR:", error)

finally:
    db.close()
