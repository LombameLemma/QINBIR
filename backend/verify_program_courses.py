import sqlite3

db = sqlite3.connect("qinbir.db")

print("=" * 60)
print("QINBIR PROGRAM-COURSE VERIFICATION")
print("=" * 60)

print()

print("TOTAL COURSES:")
print(db.execute("SELECT COUNT(*) FROM courses").fetchone()[0])

print()

print("TOTAL PROGRAM-COURSE RELATIONSHIPS:")
print(db.execute("SELECT COUNT(*) FROM program_courses").fetchone()[0])

print()
print("=" * 60)
print("COURSES PER PROGRAM")
print("=" * 60)

rows = db.execute("""
    SELECT
        p.code,
        p.name,
        COUNT(pc.course_id)
    FROM programs p
    LEFT JOIN program_courses pc
        ON p.id = pc.program_id
    GROUP BY p.id
    ORDER BY p.id
""").fetchall()

for code, name, count in rows:
    print(f"{code:8} {name:50} {count:2} courses")

print()
print("=" * 60)
print("COMPUTER SCIENCE COURSES")
print("=" * 60)

cs_courses = db.execute("""
    SELECT
        c.code,
        c.name,
        c.credit_hours
    FROM courses c
    JOIN program_courses pc
        ON c.id = pc.course_id
    JOIN programs p
        ON p.id = pc.program_id
    WHERE p.code = 'CS'
    ORDER BY c.code
""").fetchall()

for code, name, credit_hours in cs_courses:
    print(f"{code:10} {name:40} {credit_hours} credits")

print()
print(f"Computer Science total: {len(cs_courses)} courses")

db.close()

print()
print("Database connection closed.")