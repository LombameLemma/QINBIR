import sqlite3

db = sqlite3.connect("qinbir.db")

print("=" * 60)
print("QINBIR RESOURCE CHECK")
print("=" * 60)

checks = [
    ("Departments", "SELECT COUNT(*) FROM departments"),
    ("Programs", "SELECT COUNT(*) FROM programs"),
    ("Courses", "SELECT COUNT(*) FROM courses"),
    ("Student sections", "SELECT COUNT(*) FROM student_sections"),
    ("Lecturers", "SELECT COUNT(*) FROM lecturers"),
    ("Rooms", "SELECT COUNT(*) FROM rooms"),
    ("Time slots", "SELECT COUNT(*) FROM time_slots"),
    ("Availability", "SELECT COUNT(*) FROM lecturer_availability"),
    ("Requirements", "SELECT COUNT(*) FROM course_requirements"),
    ("Schedules", "SELECT COUNT(*) FROM schedules"),
    ("Schedule entries", "SELECT COUNT(*) FROM schedule_entries"),
]

for name, query in checks:
    count = db.execute(query).fetchone()[0]
    print(f"{name:<20} {count}")

db.close()