import sqlite3

DB_PATH = "qinbir.db"

# ------------------------------------------------------------
# PROGRAM ENROLLMENT SIZES
# ------------------------------------------------------------
# Approximate students per section.
# These are seed values for QINBIR scheduling tests,
# not official university enrollment figures.
# ------------------------------------------------------------

PROGRAM_SIZES = {
    # Computational and Natural Science
    "CS": 45,
    "IS": 40,
    "MATH": 35,
    "PHY": 30,
    "STAT": 35,
    "CHEM": 30,
    "BIO": 30,

    # Social Science
    "ECON": 40,
    "MGT": 45,
    "AF": 45,
    "SOC": 35,
    "PSY": 35,
    "PSIR": 35,
    "GEOG": 30,
    "SW": 30,

    # Health
    "PH": 40,
    "NUR": 35,
    "MLS": 30,
    "MID": 30,
    "PHARM": 35,
    "HI": 35,
    "NUT": 30,

    # Institute of Technology
    "SE": 45,
    "IT": 45,
    "CE": 40,
    "ECE": 40,
    "ME": 40,
    "CHE": 35,
    "IE": 35,
    "ARCH": 30,
    "CTM": 35,
}


# ------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------

db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA foreign_keys = ON")

print("=" * 70)
print("QINBIR STUDENT SECTION SEED")
print("=" * 70)

# ------------------------------------------------------------
# LOAD PROGRAMS
# ------------------------------------------------------------

program_rows = db.execute("""
    SELECT id, name, code
    FROM programs
    ORDER BY id
""").fetchall()

programs = {
    code: {
        "id": program_id,
        "name": name,
        "code": code,
    }
    for program_id, name, code in program_rows
}

print()
print(f"Programs found in database: {len(programs)}")

# ------------------------------------------------------------
# CHECK PROGRAMS
# ------------------------------------------------------------

expected_programs = set(PROGRAM_SIZES.keys())
database_programs = set(programs.keys())

missing_programs = expected_programs - database_programs
unexpected_programs = database_programs - expected_programs

if missing_programs:
    print()
    print("ERROR: Missing programs:")
    for code in sorted(missing_programs):
        print(f"  - {code}")

    db.close()
    raise SystemExit(1)

if unexpected_programs:
    print()
    print("Note: Database contains additional programs:")
    for code in sorted(unexpected_programs):
        print(f"  - {code}")

# ------------------------------------------------------------
# CREATE SECTIONS
# ------------------------------------------------------------

created = 0
existing = 0

SEMESTER = 1

print()
print("Creating Semester 1 student sections...")
print()

for code, student_count in PROGRAM_SIZES.items():

    program = programs[code]

    for year in range(1, 5):

        for section_letter in ["A", "B"]:

            section_name = f"{code}-{year}{section_letter}"

            existing_section = db.execute("""
                SELECT id
                FROM student_sections
                WHERE name = ?
                  AND program_id = ?
                  AND year = ?
                  AND semester = ?
            """, (
                section_name,
                program["id"],
                year,
                SEMESTER,
            )).fetchone()

            if existing_section:
                existing += 1
                continue

            db.execute("""
                INSERT INTO student_sections (
                    name,
                    program_id,
                    year,
                    semester,
                    student_count
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                section_name,
                program["id"],
                year,
                SEMESTER,
                student_count,
            ))

            created += 1

db.commit()

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

total_sections = db.execute("""
    SELECT COUNT(*)
    FROM student_sections
""").fetchone()[0]

print("=" * 70)
print("STUDENT SECTION SEED COMPLETE")
print("=" * 70)

print()
print(f"Programs:              {len(programs)}")
print(f"Sections created:      {created}")
print(f"Existing sections:     {existing}")
print(f"Total sections:        {total_sections}")

print()
print("SECTIONS PER PROGRAM")
print("-" * 70)

rows = db.execute("""
    SELECT
        p.code,
        p.name,
        COUNT(ss.id)
    FROM programs p
    LEFT JOIN student_sections ss
        ON p.id = ss.program_id
    GROUP BY p.id
    ORDER BY p.id
""").fetchall()

for code, name, count in rows:
    print(f"{code:8} {name:50} {count:3} sections")

print()
print("SAMPLE SECTIONS")
print("-" * 70)

sample_rows = db.execute("""
    SELECT
        ss.id,
        ss.name,
        p.code,
        ss.year,
        ss.semester,
        ss.student_count
    FROM student_sections ss
    JOIN programs p
        ON ss.program_id = p.id
    ORDER BY ss.id
    LIMIT 20
""").fetchall()

for row in sample_rows:
    print(row)

db.close()

print()
print("Database connection closed.")
print("QINBIR student sections are ready.")