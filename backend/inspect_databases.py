import sqlite3
from pathlib import Path

for db_file in sorted(Path(".").glob("*.db")):
    print(f"\n========== {db_file.name} ==========")

    try:
        connection = sqlite3.connect(str(db_file))
        tables = connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' ORDER BY name"
        ).fetchall()

        for (table,) in tables:
            count = connection.execute(
                f'SELECT COUNT(*) FROM "{table}"'
            ).fetchone()[0]
            print(f"{table}: {count}")

        connection.close()

    except Exception as error:
        print(f"ERROR: {error}")