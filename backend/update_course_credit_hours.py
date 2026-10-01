import sqlite3


DB_NAME = "qinbir.db"


# ============================================================
# COURSE CREDIT-HOUR RULES
# ============================================================
#
# 2 CH -> one 2-hour class
# 3 CH -> one 2-hour + one 1-hour class
# 4 CH -> two 2-hour classes
#
# We start conservatively:
# - Most normal lecture courses remain 3 CH.
# - Practicums, projects, laboratories, and intensive design
#   courses become 4 CH.
# - A few lighter professional/safety courses become 2 CH.
#
# This is a QINBIR scheduling dataset, not an official
# university curriculum.
# ============================================================


FOUR_CREDIT_CODES = {
    # Computer Science / Software / IT
    "CS402",
    "SE401",
    "IT402",

    # Science
    "PHY401",
    "CHEM401",
    "BIO401",

    # Health
    "PH402",
    "NUR401",
    "MLS401",
    "MLS402",
    "MID401",
    "PHARM401",
    "NUT402",

    # Engineering / Technology
    "CE401",
    "ECE402",
    "ME401",
    "CHE305",
    "CHE401",
    "IE401",
    "ARCH402",
    "CTM401",
}


TWO_CREDIT_CODES = {
    # Lighter professional / supporting courses
    "CS310",
    "MGT303",
    "MGT401",
    "PSIR309",
    "GEOG402",
    "SW308",
    "PHARM302",
    "HI203",
    "CTM304",
    "ARCH401",
}


# ============================================================
# DATABASE
# ============================================================

db = sqlite3.connect(DB_NAME)
cursor = db.cursor()

print("=" * 70)
print("QINBIR COURSE CREDIT-HOUR UPDATE")
print("=" * 70)


# ------------------------------------------------------------
# Verify all courses
# ------------------------------------------------------------

total_courses = cursor.execute(
    "SELECT COUNT(*) FROM courses"
).fetchone()[0]

print(f"\nCourses found: {total_courses}")


# ------------------------------------------------------------
# Reset all courses to the normal 3-credit value
# ------------------------------------------------------------

cursor.execute(
    """
    UPDATE courses
    SET credit_hours = 3
    """
)

print("All courses reset to 3 credit hours.")


# ------------------------------------------------------------
# Apply 4-credit courses
# ------------------------------------------------------------

four_updated = 0

for code in FOUR_CREDIT_CODES:

    cursor.execute(
        """
        UPDATE courses
        SET credit_hours = 4
        WHERE code = ?
        """,
        (code,)
    )

    if cursor.rowcount > 0:
        four_updated += cursor.rowcount
    else:
        print(f"WARNING: 4-credit course not found: {code}")


# ------------------------------------------------------------
# Apply 2-credit courses
# ------------------------------------------------------------

two_updated = 0

for code in TWO_CREDIT_CODES:

    cursor.execute(
        """
        UPDATE courses
        SET credit_hours = 2
        WHERE code = ?
        """,
        (code,)
    )

    if cursor.rowcount > 0:
        two_updated += cursor.rowcount
    else:
        print(f"WARNING: 2-credit course not found: {code}")


# ------------------------------------------------------------
# Commit
# ------------------------------------------------------------

db.commit()


# ------------------------------------------------------------
# Show distribution
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("NEW CREDIT-HOUR DISTRIBUTION")
print("=" * 70)

rows = cursor.execute(
    """
    SELECT credit_hours, COUNT(*)
    FROM courses
    GROUP BY credit_hours
    ORDER BY credit_hours
    """
).fetchall()

for credit_hours, count in rows:
    print(
        f"{credit_hours} credit hours: {count} courses"
    )


# ------------------------------------------------------------
# Show actual courses by credit
# ------------------------------------------------------------

for credit_hours in [2, 3, 4]:

    rows = cursor.execute(
        """
        SELECT code, name
        FROM courses
        WHERE credit_hours = ?
        ORDER BY code
        """,
        (credit_hours,)
    ).fetchall()

    print("\n" + "-" * 70)
    print(f"{credit_hours}-CREDIT COURSES: {len(rows)}")
    print("-" * 70)

    for code, name in rows:
        print(f"{code:10} {name}")


# ------------------------------------------------------------
# Calculate theoretical teaching hours
# ------------------------------------------------------------

total_hours = cursor.execute(
    """
    SELECT COALESCE(SUM(credit_hours), 0)
    FROM courses
    """
).fetchone()[0]

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"Total courses:          {total_courses}")
print(f"2-credit courses:       {two_updated}")
print(f"4-credit courses:       {four_updated}")
print(f"Total catalog hours:    {total_hours}")


db.close()

print("\nDatabase connection closed.")
print("Course credit-hour update complete.")