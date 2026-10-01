import sqlite3

DB_PATH = "qinbir.db"

# ---------------------------------------------------------
# Lecturer data
# 3 lecturers per program = 93 lecturers total.
# Existing lecturers LEC001 and LEC002 are preserved.
# ---------------------------------------------------------

PROGRAM_LECTURERS = {
    "CS": [
        ("Dr. Dawit Alemu", "dawit.alemu"),
        ("Dr. Meron Bekele", "meron.bekele"),
        ("Dr. Samuel Girma", "samuel.girma"),
    ],
    "IS": [
        ("Dr. Abel Tesfaye", "abel.tesfaye"),
        ("Dr. Hana Worku", "hana.worku"),
        ("Dr. Daniel Tadesse", "daniel.tadesse"),
    ],
    "MATH": [
        ("Dr. Tewodros Kebede", "tewodros.kebede"),
        ("Dr. Selamawit Getachew", "selamawit.getachew"),
        ("Dr. Yonatan Assefa", "yonatan.assefa"),
    ],
    "PHY": [
        ("Dr. Bereket Mengistu", "bereket.mengistu"),
        ("Dr. Rahel Solomon", "rahel.solomon"),
        ("Dr. Henok Abebe", "henok.abebe"),
    ],
    "STAT": [
        ("Dr. Fitsum Haile", "fitsum.haile"),
        ("Dr. Bethlehem Ayele", "bethlehem.ayele"),
        ("Dr. Natnael Girma", "natnael.girma"),
    ],
    "CHEM": [
        ("Dr. Ermias Tefera", "ermias.tefera"),
        ("Dr. Mulugeta Assefa", "mulugeta.assefa"),
        ("Dr. Tigist Worku", "tigist.worku"),
    ],
    "BIO": [
        ("Dr. Elias Fikre", "elias.fikre"),
        ("Dr. Saron Kebede", "saron.kebede"),
        ("Dr. Yonas Mekonnen", "yonas.mekonnen"),
    ],
    "ECON": [
        ("Dr. Biruk Tamiru", "biruk.tamiru"),
        ("Dr. Meseret Alemu", "meseret.alemu"),
        ("Dr. Kidist Bekele", "kidist.bekele"),
    ],
    "MGT": [
        ("Dr. Solomon Hailu", "solomon.hailu"),
        ("Dr. Kalkidan Tesfaye", "kalkidan.tesfaye"),
        ("Dr. Natnael Desta", "natnael.desta"),
    ],
    "AF": [
        ("Dr. Fasil Abate", "fasil.abate"),
        ("Dr. Almaz Girma", "almaz.girma"),
        ("Dr. Henok Tadesse", "henok.tadesse"),
    ],
    "SOC": [
        ("Dr. Alemayehu Worku", "alemayehu.worku"),
        ("Dr. Hana Girma", "hana.girma"),
        ("Dr. Eden Tesfaye", "eden.tesfaye"),
    ],
    "PSY": [
        ("Dr. Mihretu Alemu", "mihretu.alemu"),
        ("Dr. Rahel Tadesse", "rahel.tadesse"),
        ("Dr. Samuel Bekele", "samuel.bekele"),
    ],
    "PSIR": [
        ("Dr. Getachew Mulugeta", "getachew.mulugeta"),
        ("Dr. Selamawit Desta", "selamawit.desta"),
        ("Dr. Dawit Taye", "dawit.taye"),
    ],
    "GEOG": [
        ("Dr. Abiyot Mekonnen", "abiyot.mekonnen"),
        ("Dr. Hirut Alemu", "hirut.alemu"),
        ("Dr. Kenean Tesfaye", "kenean.tesfaye"),
    ],
    "SW": [
        ("Dr. Solomon Demissie", "solomon.demissie"),
        ("Dr. Martha Kebede", "martha.kebede"),
        ("Dr. Yonatan Worku", "yonatan.worku"),
    ],
    "PH": [
        ("Dr. Amanuel Gebre", "amanuel.gebre"),
        ("Dr. Bethelhem Tadesse", "bethelhem.tadesse"),
        ("Dr. Frehiwot Alemu", "frehiwot.alemu"),
    ],
    "NUR": [
        ("Dr. Abeba Solomon", "abeba.solomon"),
        ("Dr. Selam Hailu", "selam.hailu"),
        ("Dr. Natnael Kebede", "natnael.kebede"),
    ],
    "MLS": [
        ("Dr. Mastewal Girma", "mastewal.girma"),
        ("Dr. Dawit Solomon", "dawit.solomon"),
        ("Dr. Rahel Abebe", "rahel.abebe"),
    ],
    "MID": [
        ("Dr. Meseret Tadesse", "meseret.tadesse"),
        ("Dr. Tigist Kebede", "tigist.kebede"),
        ("Dr. Bethlehem Worku", "bethlehem.worku"),
    ],
    "PHARM": [
        ("Dr. Ermias Bekele", "ermias.bekele"),
        ("Dr. Selamawit Haile", "selamawit.haile"),
        ("Dr. Henok Girma", "henok.girma"),
    ],
    "HI": [
        ("Dr. Abel Mekonnen", "abel.mekonnen"),
        ("Dr. Eden Kebede", "eden.kebede"),
        ("Dr. Yonatan Tadesse", "yonatan.tadesse"),
    ],
    "NUT": [
        ("Dr. Fitsum Tesfaye", "fitsum.tesfaye"),
        ("Dr. Saron Alemu", "saron.alemu"),
        ("Dr. Bereket Worku", "bereket.worku"),
    ],
    "SE": [
        ("Dr. Michael Tadesse", "michael.tadesse"),
        ("Dr. Nahom Kebede", "nahom.kebede"),
        ("Dr. Rahel Mekonnen", "rahel.mekonnen"),
    ],
    "IT": [
        ("Dr. Henok Tadesse", "henok.tadesse.it"),
        ("Dr. Abel Girma", "abel.girma"),
        ("Dr. Meron Alemu", "meron.alemu.it"),
    ],
    "CE": [
        ("Dr. Girma Bekele", "girma.bekele"),
        ("Dr. Yared Alemu", "yared.alemu"),
        ("Dr. Kalkidan Worku", "kalkidan.worku"),
    ],
    "ECE": [
        ("Dr. Samuel Tadesse", "samuel.tadesse.ece"),
        ("Dr. Daniel Kebede", "daniel.kebede"),
        ("Dr. Bethlehem Girma", "bethlehem.girma"),
    ],
    "ME": [
        ("Dr. Tadesse Mekonnen", "tadesse.mekonnen"),
        ("Dr. Fikru Alemu", "fikru.alemu"),
        ("Dr. Selamawit Kebede", "selamawit.kebede.me"),
    ],
    "CHE": [
        ("Dr. Asrat Tadesse", "asrat.tadesse"),
        ("Dr. Henok Alemu", "henok.alemu"),
        ("Dr. Rahel Worku", "rahel.worku"),
    ],
    "IE": [
        ("Dr. Dawit Mekonnen", "dawit.mekonnen"),
        ("Dr. Kalkidan Abebe", "kalkidan.abebe"),
        ("Dr. Mihret Tesfaye", "mihret.tesfaye"),
    ],
    "ARCH": [
        ("Dr. Yonas Alemu", "yonas.alemu"),
        ("Dr. Martha Tadesse", "martha.tadesse"),
        ("Dr. Abel Worku", "abel.worku"),
    ],
    "CTM": [
        ("Dr. Solomon Kebede", "solomon.kebede"),
        ("Dr. Eden Worku", "eden.worku"),
        ("Dr. Natnael Alemu", "natnael.alemu"),
    ],
}


def main():
    print("=" * 70)
    print("QINBIR LECTURER SEED")
    print("=" * 70)

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON")

    # ---------------------------------------------------------
    # Get departments
    # ---------------------------------------------------------
    departments = {}

    rows = db.execute(
        "SELECT id, code, name FROM departments ORDER BY id"
    ).fetchall()

    for row in rows:
        department_id, code, name = row
        departments[code] = {
            "id": department_id,
            "name": name,
        }

    print()
    print(f"Departments found: {len(departments)}")

    # ---------------------------------------------------------
    # Program -> Department mapping
    # ---------------------------------------------------------
    program_rows = db.execute(
        """
        SELECT p.id, p.code, p.name, p.department_id, d.code
        FROM programs p
        JOIN departments d ON d.id = p.department_id
        ORDER BY p.id
        """
    ).fetchall()

    program_info = {}

    for row in program_rows:
        program_id, program_code, program_name, department_id, department_code = row

        program_info[program_code] = {
            "id": program_id,
            "name": program_name,
            "department_id": department_id,
            "department_code": department_code,
        }

    print(f"Programs found:    {len(program_info)}")

    # ---------------------------------------------------------
    # Verify every program has lecturer data
    # ---------------------------------------------------------
    missing = []

    for program_code in program_info:
        if program_code not in PROGRAM_LECTURERS:
            missing.append(program_code)

    if missing:
        print()
        print("ERROR: Lecturer data missing for:")
        for code in missing:
            print(f"  - {code}")

        db.close()
        return

    # ---------------------------------------------------------
    # Create/reuse users and lecturers
    # ---------------------------------------------------------
    created_users = 0
    existing_users = 0
    created_lecturers = 0
    existing_lecturers = 0

    next_employee_number = db.execute(
        """
        SELECT COALESCE(
            MAX(
                CAST(
                    REPLACE(employee_id, 'LEC', '')
                    AS INTEGER
                )
            ),
            0
        )
        FROM lecturers
        WHERE employee_id LIKE 'LEC%'
        """
    ).fetchone()[0]

    employee_number = next_employee_number

    print()
    print("Creating lecturers...")
    print("-" * 70)

    for program_code, lecturers in PROGRAM_LECTURERS.items():

        info = program_info[program_code]

        department_id = info["department_id"]
        department_code = info["department_code"]

        print(
            f"{program_code:<8} "
            f"{info['name']:<50}"
        )

        for name, username in lecturers:

            email = f"{username}@qinbir.edu.et"

            # -------------------------------------------------
            # Find or create User
            # -------------------------------------------------
            user = db.execute(
                "SELECT id FROM users WHERE email = ?",
                (email,)
            ).fetchone()

            if user:
                user_id = user[0]
                existing_users += 1
            else:
                db.execute(
                    """
                    INSERT INTO users
                    (
                        full_name,
                        email,
                        password_hash,
                        role,
                        is_active
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        name,
                        email,
                        "seed_password_hash",
                        "LECTURER",
                        1,
                    )
                )

                user_id = db.execute(
                    "SELECT last_insert_rowid()"
                ).fetchone()[0]

                created_users += 1

            # -------------------------------------------------
            # Check whether lecturer already exists
            # -------------------------------------------------
            existing = db.execute(
                """
                SELECT id
                FROM lecturers
                WHERE user_id = ?
                """,
                (user_id,)
            ).fetchone()

            if existing:
                existing_lecturers += 1
                continue

            # -------------------------------------------------
            # Create lecturer
            # -------------------------------------------------
            employee_number += 1
            employee_id = f"LEC{employee_number:03d}"

            db.execute(
                """
                INSERT INTO lecturers
                (
                    user_id,
                    department_id,
                    employee_id,
                    name
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    user_id,
                    department_id,
                    employee_id,
                    name,
                )
            )

            created_lecturers += 1

    db.commit()

    # ---------------------------------------------------------
    # Final statistics
    # ---------------------------------------------------------
    total_users = db.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    total_lecturers = db.execute(
        "SELECT COUNT(*) FROM lecturers"
    ).fetchone()[0]

    print()
    print("=" * 70)
    print("LECTURER SEED COMPLETE")
    print("=" * 70)

    print(f"Users created:          {created_users}")
    print(f"Users already existed:  {existing_users}")
    print()
    print(f"Lecturers created:      {created_lecturers}")
    print(f"Lecturers already exist:{existing_lecturers}")
    print()
    print(f"Total users:            {total_users}")
    print(f"Total lecturers:        {total_lecturers}")

    # ---------------------------------------------------------
    # Department summary
    # ---------------------------------------------------------
    print()
    print("LECTURERS PER DEPARTMENT")
    print("-" * 70)

    department_counts = db.execute(
        """
        SELECT
            d.code,
            d.name,
            COUNT(l.id)
        FROM departments d
        LEFT JOIN lecturers l
            ON l.department_id = d.id
        GROUP BY d.id
        ORDER BY d.id
        """
    ).fetchall()

    for code, name, count in department_counts:
        print(
            f"{code:<8} "
            f"{name:<45} "
            f"{count:>3} lecturers"
        )

    db.close()

    print()
    print("Database connection closed.")
    print("QINBIR lecturers are ready.")


if __name__ == "__main__":
    main()