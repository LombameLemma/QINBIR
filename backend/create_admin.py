
from getpass import getpass

from sqlalchemy import inspect

from app.database import SessionLocal, engine
from app.models.user import User
from app.security import hash_password


def main():
    inspector = inspect(engine)

    if not inspector.has_table("users"):
        print("ERROR: The users table does not exist. Nothing changed.")
        return

    db = SessionLocal()

    try:
        existing_admin = (
            db.query(User)
            .filter(User.role.ilike("ADMIN"))
            .first()
        )

        if existing_admin:
            print(
                f"An Admin already exists: {existing_admin.email}"
            )
            print("No account was created or modified.")
            return

        print("Create the initial QINBIR Admin account.")
        print("This will not modify existing lecturer accounts.")

        full_name = input("Admin full name: ").strip()
        email = input("Admin email: ").strip().lower()

        if not full_name or not email or "@" not in email:
            print("ERROR: Enter a valid name and email.")
            return

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            print(
                "ERROR: This email already belongs to an account."
            )
            print("No account was created or modified.")
            return

        password = getpass("Admin password (minimum 12 characters): ")
        confirmation = getpass("Confirm Admin password: ")

        if len(password) < 12:
            print("ERROR: Use at least 12 characters.")
            return

        if password != confirmation:
            print("ERROR: Passwords do not match.")
            return

        admin = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role="ADMIN",
            is_active=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("\nAdmin account created successfully.")
        print("Admin ID:", admin.id)
        print("Admin email:", admin.email)
        print("Role:", admin.role)
        print("Password stored as a hash.")

    except Exception:
        db.rollback()
        print("ERROR: Admin creation failed. Database changes rolled back.")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
