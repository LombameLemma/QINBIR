import sqlite3

db = sqlite3.connect("qinbir.db")

rows = db.execute("""
    SELECT
        credit_hours,
        COUNT(*) AS course_count
    FROM courses
    GROUP BY credit_hours
    ORDER BY credit_hours
""").fetchall()

print()
print("COURSE CREDIT-HOUR DISTRIBUTION")
print("=" * 50)

for credit_hours, count in rows:
    print(f"{credit_hours} credit hours: {count} courses")

db.close()