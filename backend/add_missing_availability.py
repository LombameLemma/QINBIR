import sqlite3

DB_PATH = "qinbir.db"


def main():
    db = sqlite3.connect(DB_PATH)

    print("=" * 70)
    print("QINBIR MISSING LECTURER AVAILABILITY FIX")
    print("=" * 70)

    # --------------------------------------------------------
    # Load lecturers
    # --------------------------------------------------------

    lecturers = db.execute(
        """
        SELECT id, name
        FROM lecturers
        ORDER BY id
        """
    ).fetchall()

    # --------------------------------------------------------
    # Load time slots
    # --------------------------------------------------------

    time_slots = db.execute(
        """
        SELECT id, day, start_time, end_time
        FROM time_slots
        ORDER BY id
        """
    ).fetchall()

    print()
    print(f"Lecturers:   {len(lecturers)}")
    print(f"Time slots:  {len(time_slots)}")

    expected = len(lecturers) * len(time_slots)

    print(f"Expected availability records: {expected}")

    # --------------------------------------------------------
    # Find missing records
    # --------------------------------------------------------

    missing = []

    for lecturer_id, lecturer_name in lecturers:

        for slot_id, day, start_time, end_time in time_slots:

            existing = db.execute(
                """
                SELECT id
                FROM lecturer_availability
                WHERE lecturer_id = ?
                  AND time_slot_id = ?
                """,
                (
                    lecturer_id,
                    slot_id,
                ),
            ).fetchone()

            if existing is None:
                missing.append(
                    (
                        lecturer_id,
                        slot_id,
                    )
                )

    print()
    print(f"Missing availability records: {len(missing)}")

    # --------------------------------------------------------
    # Add missing records
    # --------------------------------------------------------

    if not missing:
        print()
        print("No missing availability records.")
        db.close()
        return

    db.executemany(
        """
        INSERT INTO lecturer_availability
        (
            lecturer_id,
            time_slot_id,
            is_available
        )
        VALUES (?, ?, 1)
        """,
        missing,
    )

    db.commit()

    # --------------------------------------------------------
    # Verify
    # --------------------------------------------------------

    final_count = db.execute(
        """
        SELECT COUNT(*)
        FROM lecturer_availability
        """
    ).fetchone()[0]

    print()
    print("=" * 70)
    print("AVAILABILITY FIX COMPLETE")
    print("=" * 70)

    print(f"Records added:       {len(missing)}")
    print(f"Total availability:  {final_count}")
    print(f"Expected:            {expected}")

    if final_count == expected:
        print()
        print("SUCCESS: All lecturers have availability records.")
    else:
        print()
        print("WARNING: Availability count does not match expected.")

    db.close()

    print()
    print("Database connection closed.")


if __name__ == "__main__":
    main()