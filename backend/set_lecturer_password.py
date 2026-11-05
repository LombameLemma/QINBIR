from getpass import getpass

from sqlalchemy import inspect

from app.database import SessionLocal, engine
from app.models.user import User
from app.models.lecturer import Lecturer
from app.security import hash_password


def main():
    if not inspect(engine).has_table("users"):
        print("ERROR: Users table not found. Nothing changed.")
        return

    db = SessionLocal()

    try:
        print("QINBIR — Set a lecturer password")
        print("No lecturer profile or schedule will be changed.")
        print()

        email = input("Lecturer email: ").strip().lower()

        account = db.query(User).filter(
            User.email == email
        ).first()

        if account is None:
            print("ERROR: No account exists with that email.")
            return

        if account.role.upper() != "LECTURER":
            print("ERROR: This account is not a lecturer account.")
            return

        lecturer = db.query(Lecturer).filter(
            Lecturer.user_id == account.id
        ).first()

        if lecturer is None:
            print("ERROR: No lecturer profile is linked to this account.")
            return

        print(f"Lecturer: {lecturer.name}")
        print(f"Email: {account.email}")

        password = getpass("New password (minimum 12 characters): ")
        confirmation = getpass("Confirm new password: ")

        if len(password) < 12:
            print("ERROR: Use at least 12 characters. Nothing changed.")
            return

        if password != confirmation:
            print("ERROR: Passwords do not match. Nothing changed.")
            return

        confirm = input(
            "Type SET PASSWORD to confirm this account change: "
        ).strip()

        if confirm != "SET PASSWORD":
            print("Cancelled. Nothing changed.")
            return

        account.password_hash = hash_password(password)
        db.commit()

        print()
        print("SUCCESS: Lecturer password updated.")
        print("The password was stored as a hash.")
        print("No other account was modified.")

    except Exception:
        db.rollback()
        print("ERROR: Password update failed. Changes were rolled back.")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
