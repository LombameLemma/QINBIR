from getpass import getpass

from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password

LECTURER_IDS = [1,48, 49, 50]

db = SessionLocal()

try:
    users = (
        db.query(User)
        .filter(
            User.id.in_(LECTURER_IDS),
            User.role == "LECTURER",
        )
        .order_by(User.id)
        .all()
    )

    if len(users) != len(LECTURER_IDS):
        raise RuntimeError(
            "Expected lecturer accounts were not all found. No changes made."
        )

    print("\nLECTURER PASSWORD RESET")
    print("-----------------------")

    for user in users:
        print(f"{user.id}: {user.full_name} ({user.email})")

    print("\nEnter a new password for each lecturer.")
    print("Passwords must contain at least 8 characters.")
    print("Passwords will not be displayed.")

    new_hashes = {}

    for user in users:
        while True:
            password = getpass(
                f"\nNew password for {user.email}: "
            )

            if len(password) < 8:
                print("Password must contain at least 8 characters.")
                continue

            if len(password.encode("utf-8")) > 72:
                print("Password must be no more than 72 UTF-8 bytes.")
                continue

            confirmation = getpass("Confirm new password: ")

            if password != confirmation:
                print("Passwords do not match. Try again.")
                continue

            new_hashes[user.id] = hash_password(password)
            break

    confirm = input(
        "\nType RESET to update only these three accounts: "
    )

    if confirm != "RESET":
        print("Cancelled. No changes were made.")
    else:
        for user in users:
            user.password_hash = new_hashes[user.id]

        db.commit()
        print("\nSUCCESS: Three lecturer passwords were updated.")

except Exception:
    db.rollback()
    raise

finally:
    db.close()
