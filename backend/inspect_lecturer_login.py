import sqlite3

db = sqlite3.connect("qinbir.db")

print("LECTURER LOGIN ACCOUNT CHECK")
print("-" * 45)

rows = db.execute("""
    SELECT id, email, role, is_active, password_hash
    FROM users
    WHERE role = 'LECTURER'
    ORDER BY id
""").fetchall()

print("Total lecturer accounts:", len(rows))

formats = {}

for user_id, email, role, active, password_hash in rows:
    if password_hash.startswith("$2"):
        fmt = "bcrypt"
    elif password_hash.startswith("pbkdf2:"):
        fmt = "pbkdf2"
    else:
        fmt = "unknown/placeholder"

    formats[fmt] = formats.get(fmt, 0) + 1

    print(
        f"ID: {user_id} | {email} | "
        f"Active: {active} | Hash format: {fmt}"
    )

print("\nHASH FORMAT SUMMARY:")
for fmt, count in formats.items():
    print(f"{fmt}: {count}")

db.close()