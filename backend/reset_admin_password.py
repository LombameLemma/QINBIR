from getpass import getpass

from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password

db = SessionLocal()

try:
    user = db.query(User).filter(
        User.email == "admin@gmail.com"
    ).first()

    if user is None:
        print("Admin account not found.")
    else:
        password = getpass("Enter your NEW Admin password: ")
        confirmation = getpass("Confirm your NEW Admin password: ")

        if len(password) < 8:
            print("Password must contain at least 8 characters.")
        elif password != confirmation:
            print("Passwords do not match.")
        else:
            user.password_hash = hash_password(password)
            db.commit()
            print("Admin password updated successfully!")

finally:
    db.close()
