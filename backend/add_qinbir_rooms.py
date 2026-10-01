import sqlite3

DB_PATH = "qinbir.db"
TARGET_ROOMS = 110


def main():
    db = sqlite3.connect(DB_PATH)

    current_rooms = db.execute(
        "SELECT COUNT(*) FROM rooms"
    ).fetchone()[0]

    print("=" * 70)
    print("QINBIR ROOM EXPANSION")
    print("=" * 70)

    print(f"Current rooms: {current_rooms}")
    print(f"Target rooms:  {TARGET_ROOMS}")

    rooms_to_add = max(
        0,
        TARGET_ROOMS - current_rooms
    )

    print(f"Rooms to add:  {rooms_to_add}")

    if rooms_to_add == 0:
        print()
        print("Room count is already correct.")
        db.close()
        return

    buildings = [
        "Main Building",
        "Science Building",
        "Technology Building",
        "Engineering Building",
        "Health Sciences Building",
        "Social Sciences Building",
    ]

    capacities = [
        30,
        30,
        35,
        35,
        40,
        40,
        45,
        45,
        50,
        50,
        55,
        60,
        60,
        70,
        80,
    ]

    room_types = [
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "CLASSROOM",
        "LECTURE_HALL",
        "LAB",
    ]

    next_number = current_rooms + 1

    for index in range(rooms_to_add):

        room_number = next_number + index

        building = buildings[
            index % len(buildings)
        ]

        capacity = capacities[
            index % len(capacities)
        ]

        room_type = room_types[
            index % len(room_types)
        ]

        room_name = f"Room {room_number:03d}"

        db.execute(
            """
            INSERT INTO rooms
            (
                name,
                building,
                capacity,
                room_type
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                room_name,
                building,
                capacity,
                room_type,
            ),
        )

    db.commit()

    final_count = db.execute(
        "SELECT COUNT(*) FROM rooms"
    ).fetchone()[0]

    print()
    print("=" * 70)
    print("ROOM EXPANSION COMPLETE")
    print("=" * 70)

    print(f"Rooms added:  {rooms_to_add}")
    print(f"Total rooms:  {final_count}")

    db.close()


if __name__ == "__main__":
    main()