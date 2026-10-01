import sqlite3
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from pulp import (
    LpProblem,
    LpVariable,
    LpMinimize,
    LpBinary,
    lpSum,
    LpStatus,
    PULP_CBC_CMD,
)


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "qinbir.db"


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# TIME HELPERS
# ============================================================

def time_to_minutes(value):
    if value is None:
        return 0

    value = str(value)
    parts = value.split(":")

    return int(parts[0]) * 60 + int(parts[1])


def slots_overlap(slot_a, slot_b):
    if slot_a["day"] != slot_b["day"]:
        return False

    a_start = time_to_minutes(slot_a["start_time"])
    a_end = time_to_minutes(slot_a["end_time"])

    b_start = time_to_minutes(slot_b["start_time"])
    b_end = time_to_minutes(slot_b["end_time"])

    return (
        a_start < b_end
        and b_start < a_end
    )


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    db = get_connection()
    db.row_factory = sqlite3.Row

    requirements = db.execute("""
        SELECT
            cr.id,
            cr.course_id,
            cr.student_section_id,
            cr.lecturer_id,
            cr.sessions_per_week,
            cr.long_session_hours,
            cr.short_session_hours,

            c.code AS course_code,
            c.name AS course_name,
            c.credit_hours,

            ss.name AS section_name,
            ss.student_count,

            l.name AS lecturer_name

        FROM course_requirements cr

        JOIN courses c
            ON c.id = cr.course_id

        JOIN student_sections ss
            ON ss.id = cr.student_section_id

        JOIN lecturers l
            ON l.id = cr.lecturer_id

        ORDER BY cr.id
    """).fetchall()

    rooms = db.execute("""
        SELECT
            id,
            name,
            building,
            capacity,
            room_type
        FROM rooms
        ORDER BY capacity, id
    """).fetchall()

    time_slots = db.execute("""
        SELECT
            id,
            day,
            start_time,
            end_time
        FROM time_slots
        ORDER BY
            CASE day
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
                WHEN 'Saturday' THEN 6
                WHEN 'Sunday' THEN 7
                ELSE 8
            END,
            start_time
    """).fetchall()

    availability_rows = db.execute("""
        SELECT
            lecturer_id,
            time_slot_id,
            is_available
        FROM lecturer_availability
    """).fetchall()

    db.close()

    availability = {
        (
            row["lecturer_id"],
            row["time_slot_id"]
        ): bool(row["is_available"])
        for row in availability_rows
    }

    return {
        "requirements": requirements,
        "rooms": rooms,
        "time_slots": time_slots,
        "availability": availability,
    }


# ============================================================
# SLOT GROUPS
# ============================================================

def build_slot_groups(time_slots):
    long_slots = []
    short_slots = []

    for slot in time_slots:

        start = time_to_minutes(
            slot["start_time"]
        )

        end = time_to_minutes(
            slot["end_time"]
        )

        duration = end - start

        if duration == 120:
            long_slots.append(slot)

        elif duration == 60:
            short_slots.append(slot)

    return long_slots, short_slots


# ============================================================
# BUILD TIME CANDIDATES
# ============================================================

def build_candidates(
    requirements,
    long_slots,
    short_slots,
    availability,
):
    """
    Build TIME candidates according to course credit hours.

    Credit-hour rules:

        2 credits
            -> 1 x 2-hour session

        3 credits
            -> 1 x 2-hour session
            -> 1 x 1-hour session

        4 credits
            -> 2 x 2-hour sessions

    Rooms are intentionally NOT included here.
    """

    long_candidates = []
    short_candidates = []

    for requirement in requirements:

        requirement_id = requirement["id"]
        lecturer_id = requirement["lecturer_id"]
        credit_hours = int(
            requirement["credit_hours"]
        )

        # ====================================================
        # 2-HOUR CANDIDATES
        # ====================================================

        if credit_hours in (2, 3, 4):

            for slot in long_slots:

                if not availability.get(
                    (
                        lecturer_id,
                        slot["id"]
                    ),
                    False
                ):
                    continue

                long_candidates.append(
                    (
                        requirement_id,
                        slot["id"]
                    )
                )

        # ====================================================
        # 1-HOUR CANDIDATES
        # ====================================================

        if credit_hours == 3:

            for slot in short_slots:

                if not availability.get(
                    (
                        lecturer_id,
                        slot["id"]
                    ),
                    False
                ):
                    continue

                short_candidates.append(
                    (
                        requirement_id,
                        slot["id"]
                    )
                )

    return (
        long_candidates,
        short_candidates
    )


# ============================================================
# BUILD MODEL
# ============================================================

def build_model(
    requirements,
    time_slots,
    long_candidates,
    short_candidates,
):
    """
    Build compact time-only scheduling model.

    Credit-hour rules:

        2 credits:
            1 x 2-hour session

        3 credits:
            1 x 2-hour session
            1 x 1-hour session
            on different days

        4 credits:
            2 x 2-hour sessions
            on different days

    Rooms are assigned after CBC finishes.
    """

    model = LpProblem(
        "QINBIR_Time_Scheduler",
        LpMinimize
    )

    slot_by_id = {
        slot["id"]: slot
        for slot in time_slots
    }

    requirement_by_id = {
        requirement["id"]: requirement
        for requirement in requirements
    }

    # ========================================================
    # VARIABLES
    # ========================================================

    long_vars = {}

    for index, candidate in enumerate(
        long_candidates
    ):

        requirement_id, slot_id = candidate

        long_vars[candidate] = LpVariable(
            f"L_{requirement_id}_{slot_id}_{index}",
            cat=LpBinary
        )

    short_vars = {}

    for index, candidate in enumerate(
        short_candidates
    ):

        requirement_id, slot_id = candidate

        short_vars[candidate] = LpVariable(
            f"S_{requirement_id}_{slot_id}_{index}",
            cat=LpBinary
        )

    # ========================================================
    # OBJECTIVE
    # ========================================================

    model += 0

    # ========================================================
    # REQUIREMENT INDEXES
    # ========================================================

    long_by_requirement = defaultdict(list)
    short_by_requirement = defaultdict(list)

    for candidate, variable in long_vars.items():

        long_by_requirement[
            candidate[0]
        ].append(variable)

    for candidate, variable in short_vars.items():

        short_by_requirement[
            candidate[0]
        ].append(variable)

    # ========================================================
    # CREDIT-HOUR SESSION REQUIREMENTS
    # ========================================================
    #
    # 2 credits:
    #     1 x 2-hour session
    #
    # 3 credits:
    #     1 x 2-hour session
    #     1 x 1-hour session
    #
    # 4 credits:
    #     2 x 2-hour sessions
    #
    # ========================================================

    for requirement in requirements:

        requirement_id = requirement["id"]

        credit_hours = int(
            requirement["credit_hours"]
        )

        long_variables = (
            long_by_requirement.get(
                requirement_id,
                []
            )
        )

        short_variables = (
            short_by_requirement.get(
                requirement_id,
                []
            )
        )

        # ----------------------------------------------------
        # 2 CREDIT COURSE
        # ----------------------------------------------------

        if credit_hours == 2:

            model += (
                lpSum(long_variables) == 1,
                f"LongSession_{requirement_id}"
            )

            model += (
                lpSum(short_variables) == 0,
                f"ShortSession_{requirement_id}"
            )

        # ----------------------------------------------------
        # 3 CREDIT COURSE
        # ----------------------------------------------------

        elif credit_hours == 3:

            model += (
                lpSum(long_variables) == 1,
                f"LongSession_{requirement_id}"
            )

            model += (
                lpSum(short_variables) == 1,
                f"ShortSession_{requirement_id}"
            )

        # ----------------------------------------------------
        # 4 CREDIT COURSE
        # ----------------------------------------------------

        elif credit_hours == 4:

            model += (
                lpSum(long_variables) == 2,
                f"LongSession_{requirement_id}"
            )

            model += (
                lpSum(short_variables) == 0,
                f"ShortSession_{requirement_id}"
            )

        else:

            raise RuntimeError(
                f"Unsupported credit hours: "
                f"{credit_hours} "
                f"for requirement "
                f"{requirement_id}"
            )

    # ========================================================
    # DIFFERENT-DAY INDEXES
    # ========================================================

    long_by_requirement_day = defaultdict(list)
    short_by_requirement_day = defaultdict(list)

    for candidate, variable in long_vars.items():

        requirement_id, slot_id = candidate

        day = slot_by_id[
            slot_id
        ]["day"]

        long_by_requirement_day[
            (
                requirement_id,
                day
            )
        ].append(variable)

    for candidate, variable in short_vars.items():

        requirement_id, slot_id = candidate

        day = slot_by_id[
            slot_id
        ]["day"]

        short_by_requirement_day[
            (
                requirement_id,
                day
            )
        ].append(variable)

    days = sorted(
        {
            slot["day"]
            for slot in time_slots
        }
    )

    # ========================================================
    # DIFFERENT-DAY CONSTRAINT
    # ========================================================

    for requirement in requirements:

        requirement_id = requirement["id"]

        credit_hours = int(
            requirement["credit_hours"]
        )

        for day in days:

            long_variables = (
                long_by_requirement_day.get(
                    (
                        requirement_id,
                        day
                    ),
                    []
                )
            )

            short_variables = (
                short_by_requirement_day.get(
                    (
                        requirement_id,
                        day
                    ),
                    []
                )
            )

            # ------------------------------------------------
            # 3 CREDIT
            # ------------------------------------------------
            #
            # Long + short must be on different days.
            #

            if credit_hours == 3:

                if (
                    long_variables
                    or short_variables
                ):

                    model += (
                        lpSum(long_variables)
                        +
                        lpSum(short_variables)
                        <= 1,
                        (
                            f"DifferentDay_"
                            f"{requirement_id}_"
                            f"{day}"
                        )
                    )

            # ------------------------------------------------
            # 4 CREDIT
            # ------------------------------------------------
            #
            # Two long sessions must be
            # on different days.
            #

            elif credit_hours == 4:

                if long_variables:

                    model += (
                        lpSum(long_variables)
                        <= 1,
                        (
                            f"DifferentDay_"
                            f"{requirement_id}_"
                            f"{day}"
                        )
                    )

    # ========================================================
    # RESOURCE / SLOT INDEX
    # ========================================================
    #
    # Resources:
    #
    #     Lecturer
    #     Student section
    #
    # Rooms are NOT included in CBC.
    #
    # ========================================================

    resource_slot = defaultdict(list)

    # --------------------------------------------------------
    # Long sessions
    # --------------------------------------------------------

    for candidate, variable in long_vars.items():

        requirement_id, slot_id = candidate

        requirement = (
            requirement_by_id[
                requirement_id
            ]
        )

        lecturer_id = (
            requirement["lecturer_id"]
        )

        section_id = (
            requirement["student_section_id"]
        )

        resource_slot[
            (
                "lecturer",
                lecturer_id,
                slot_id
            )
        ].append(variable)

        resource_slot[
            (
                "section",
                section_id,
                slot_id
            )
        ].append(variable)

    # --------------------------------------------------------
    # Short sessions
    # --------------------------------------------------------

    for candidate, variable in short_vars.items():

        requirement_id, slot_id = candidate

        requirement = (
            requirement_by_id[
                requirement_id
            ]
        )

        lecturer_id = (
            requirement["lecturer_id"]
        )

        section_id = (
            requirement["student_section_id"]
        )

        resource_slot[
            (
                "lecturer",
                lecturer_id,
                slot_id
            )
        ].append(variable)

        resource_slot[
            (
                "section",
                section_id,
                slot_id
            )
        ].append(variable)

    # ========================================================
    # SAME SLOT CONFLICTS
    # ========================================================

    for (
        resource_type,
        resource_id,
        slot_id
    ), variables in resource_slot.items():

        if len(variables) <= 1:
            continue

        model += (
            lpSum(variables) <= 1,
            (
                f"SameSlot_"
                f"{resource_type}_"
                f"{resource_id}_"
                f"{slot_id}"
            )
        )

    # ========================================================
    # OVERLAPPING SLOT PAIRS
    # ========================================================

    slot_ids = list(
        slot_by_id.keys()
    )

    overlapping_pairs = []

    for i, slot_id_a in enumerate(
        slot_ids
    ):

        slot_a = slot_by_id[
            slot_id_a
        ]

        for slot_id_b in slot_ids[
            i + 1:
        ]:

            slot_b = slot_by_id[
                slot_id_b
            ]

            if slots_overlap(
                slot_a,
                slot_b
            ):

                overlapping_pairs.append(
                    (
                        slot_id_a,
                        slot_id_b
                    )
                )

    print(
        "Overlapping slot pairs: "
        f"{len(overlapping_pairs)}"
    )

    # ========================================================
    # OVERLAP CONSTRAINTS
    # ========================================================

    for (
        slot_id_a,
        slot_id_b
    ) in overlapping_pairs:

        resources_a = defaultdict(list)
        resources_b = defaultdict(list)

        for (
            resource_type,
            resource_id,
            slot_id
        ), variables in resource_slot.items():

            if slot_id == slot_id_a:

                resources_a[
                    (
                        resource_type,
                        resource_id
                    )
                ].extend(
                    variables
                )

            elif slot_id == slot_id_b:

                resources_b[
                    (
                        resource_type,
                        resource_id
                    )
                ].extend(
                    variables
                )

        common_resources = (
            set(resources_a.keys())
            &
            set(resources_b.keys())
        )

        for resource in common_resources:

            variables = (
                resources_a[resource]
                +
                resources_b[resource]
            )

            resource_type, resource_id = (
                resource
            )

            model += (
                lpSum(variables) <= 1,
                (
                    f"Overlap_"
                    f"{resource_type}_"
                    f"{resource_id}_"
                    f"{slot_id_a}_"
                    f"{slot_id_b}"
                )
            )

    print(
        "Decision variables: "
        f"{len(model.variables()):,}"
    )

    print(
        "Constraints: "
        f"{len(model.constraints):,}"
    )

    return (
        model,
        long_vars,
        short_vars
    )


# ============================================================
# SOLVE
# ============================================================

def solve_model(model):

    print()
    print("=" * 60)
    print("STARTING CBC")
    print("=" * 60)

    solver = PULP_CBC_CMD(
        msg=True
    )

    status = model.solve(
        solver
    )

    print()
    print(
        "SOLVER STATUS:",
        LpStatus[model.status]
    )

    return status


# ============================================================
# EXTRACT SOLUTION
# ============================================================

def extract_sessions(
    requirements,
    time_slots,
    long_vars,
    short_vars,
):
    """
    Extract selected sessions from CBC.
    """

    requirement_by_id = {
        requirement["id"]: requirement
        for requirement in requirements
    }

    slot_by_id = {
        slot["id"]: slot
        for slot in time_slots
    }

    sessions = []

    # ========================================================
    # LONG SESSIONS
    # ========================================================

    for candidate, variable in long_vars.items():

        if variable.value() != 1:
            continue

        requirement_id, slot_id = candidate

        requirement = (
            requirement_by_id[
                requirement_id
            ]
        )

        slot = slot_by_id[
            slot_id
        ]

        sessions.append({
            "requirement_id": requirement_id,
            "lecturer_id": requirement[
                "lecturer_id"
            ],
            "student_section_id": (
                requirement[
                    "student_section_id"
                ]
            ),
            "student_count": requirement[
                "student_count"
            ],
            "course_code": requirement[
                "course_code"
            ],
            "course_name": requirement[
                "course_name"
            ],
            "lecturer_name": requirement[
                "lecturer_name"
            ],
            "section_name": requirement[
                "section_name"
            ],
            "credit_hours": int(
                requirement[
                    "credit_hours"
                ]
            ),
            "slot_id": slot_id,
            "day": slot["day"],
            "start_time": slot[
                "start_time"
            ],
            "end_time": slot[
                "end_time"
            ],
            "duration": 2,
        })

    # ========================================================
    # SHORT SESSIONS
    # ========================================================

    for candidate, variable in short_vars.items():

        if variable.value() != 1:
            continue

        requirement_id, slot_id = candidate

        requirement = (
            requirement_by_id[
                requirement_id
            ]
        )

        slot = slot_by_id[
            slot_id
        ]

        sessions.append({
            "requirement_id": requirement_id,
            "lecturer_id": requirement[
                "lecturer_id"
            ],
            "student_section_id": (
                requirement[
                    "student_section_id"
                ]
            ),
            "student_count": requirement[
                "student_count"
            ],
            "course_code": requirement[
                "course_code"
            ],
            "course_name": requirement[
                "course_name"
            ],
            "lecturer_name": requirement[
                "lecturer_name"
            ],
            "section_name": requirement[
                "section_name"
            ],
            "credit_hours": int(
                requirement[
                    "credit_hours"
                ]
            ),
            "slot_id": slot_id,
            "day": slot["day"],
            "start_time": slot[
                "start_time"
            ],
            "end_time": slot[
                "end_time"
            ],
            "duration": 1,
        })

    return sessions


# ============================================================
# ROOM ASSIGNMENT
# ============================================================

def assign_rooms(
    sessions,
    rooms,
    time_slots
):
    """
    Assign rooms AFTER the time schedule is solved.

    Rooms are selected by:
        1. capacity
        2. room availability
        3. smallest suitable room first

    Sessions are processed from largest classes
    to smallest classes.
    """

    slot_by_id = {
        slot["id"]: slot
        for slot in time_slots
    }

    # ========================================================
    # SORT SESSIONS
    # ========================================================

    def session_sort_key(session):

        slot = slot_by_id[
            session["slot_id"]
        ]

        return (
            session["day"],
            time_to_minutes(
                slot["start_time"]
            ),
            -session["student_count"],
            -session["duration"],
        )

    ordered_sessions = sorted(
        sessions,
        key=session_sort_key
    )

    # ========================================================
    # ROOM AVAILABILITY
    # ========================================================

    room_schedule = defaultdict(list)

    # ========================================================
    # PROCESS SESSIONS
    # ========================================================

    for session in ordered_sessions:

        slot = slot_by_id[
            session["slot_id"]
        ]

        suitable_rooms = [
            room
            for room in rooms
            if room["capacity"]
            >= session["student_count"]
        ]

        suitable_rooms.sort(
            key=lambda room: (
                room["capacity"],
                room["id"]
            )
        )

        selected_room = None

        for room in suitable_rooms:

            conflicts = False

            for existing_slot_id in (
                room_schedule[
                    room["id"]
                ]
            ):

                existing_slot = slot_by_id[
                    existing_slot_id
                ]

                if slots_overlap(
                    slot,
                    existing_slot
                ):

                    conflicts = True
                    break

            if not conflicts:

                selected_room = room
                break

        if selected_room is None:

            raise RuntimeError(
                "ROOM ASSIGNMENT FAILED.\n"
                f"Course: "
                f"{session['course_code']} "
                f"{session['course_name']}\n"
                f"Section: "
                f"{session['section_name']}\n"
                f"Students: "
                f"{session['student_count']}\n"
                f"Day: "
                f"{session['day']}\n"
                f"Time: "
                f"{session['start_time']} - "
                f"{session['end_time']}\n"
                "No suitable room was available."
            )

        session["room_id"] = (
            selected_room["id"]
        )

        session["room_name"] = (
            selected_room["name"]
        )

        session["room_building"] = (
            selected_room["building"]
        )

        session["room_capacity"] = (
            selected_room["capacity"]
        )

        room_schedule[
            selected_room["id"]
        ].append(
            session["slot_id"]
        )

    return ordered_sessions


# ============================================================
# SAVE SCHEDULE
# ============================================================

def save_schedule(sessions):
    """
    Delete previous automatic schedule
    and save the new one.
    """

    db = get_connection()

    # ========================================================
    # DELETE PREVIOUS AUTOMATIC SCHEDULES
    # ========================================================

    old_schedules = db.execute("""
        SELECT id
        FROM schedules
        WHERE name =
        'Automatically Generated Schedule'
    """).fetchall()

    for row in old_schedules:

        schedule_id = row[0]

        db.execute("""
            DELETE FROM schedule_entries
            WHERE schedule_id = ?
        """, (
            schedule_id,
        ))

        db.execute("""
            DELETE FROM schedules
            WHERE id = ?
        """, (
            schedule_id,
        ))

    # ========================================================
    # CREATE SCHEDULE
    # ========================================================

    cursor = db.execute("""
        INSERT INTO schedules (
            name,
            status,
            created_at
        )
        VALUES (?, ?, ?)
    """, (
        "Automatically Generated Schedule",
        "DRAFT",
        datetime.utcnow().isoformat()
    ))

    schedule_id = cursor.lastrowid

    # ========================================================
    # INSERT ENTRIES
    # ========================================================

    entries = []

    for session in sessions:

        entries.append((
            schedule_id,
            session["requirement_id"],
            session["lecturer_id"],
            session[
                "student_section_id"
            ],
            session["room_id"],
            session["slot_id"],
        ))

    db.executemany("""
        INSERT INTO schedule_entries (
            schedule_id,
            course_requirement_id,
            lecturer_id,
            student_section_id,
            room_id,
            time_slot_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, entries)

    db.commit()
    db.close()

    return (
        schedule_id,
        len(entries)
    )


# ============================================================
# VALIDATE SCHEDULE
# ============================================================

def validate_schedule(sessions):
    """
    Perform credit-aware validation.

    Rules:

        2 credits:
            exactly 1 x 2-hour session

        3 credits:
            exactly 1 x 2-hour session
            exactly 1 x 1-hour session
            different days

        4 credits:
            exactly 2 x 2-hour sessions
            different days
    """

    # ========================================================
    # GROUP SESSIONS BY REQUIREMENT
    # ========================================================

    requirement_sessions = defaultdict(list)

    for session in sessions:

        requirement_sessions[
            session["requirement_id"]
        ].append(session)

    # ========================================================
    # BASIC CREDIT-HOUR VALIDATION
    # ========================================================

    for requirement_id, values in (
        requirement_sessions.items()
    ):

        credit_hours = int(
            values[0]["credit_hours"]
        )

        durations = [
            value["duration"]
            for value in values
        ]

        days_for_requirement = {
            value["day"]
            for value in values
        }

        # ----------------------------------------------------
        # 2 CREDIT
        # ----------------------------------------------------

        if credit_hours == 2:

            if len(values) != 1:

                raise RuntimeError(
                    "Validation failed: "
                    f"requirement "
                    f"{requirement_id} "
                    "must have exactly "
                    "one session."
                )

            if durations != [2]:

                raise RuntimeError(
                    "Validation failed: "
                    f"requirement "
                    f"{requirement_id} "
                    "must have one 2-hour "
                    "session."
                )

        # ----------------------------------------------------
        # 3 CREDIT
        # ----------------------------------------------------

        elif credit_hours == 3:

            if len(values) != 2:

                raise RuntimeError(
                    "Validation failed: "
                    f"requirement "
                    f"{requirement_id} "
                    "must have exactly "
                    "two sessions."
                )

            if sorted(durations) != [1, 2]:

                raise RuntimeError(
                    "Validation failed: "
                    f"requirement "
                    f"{requirement_id} "
                    "must have one 2-hour "
                    "and one 1-hour session."
                )

            if len(days_for_requirement) != 2:

                raise RuntimeError(
                    "Validation failed: "
                    f"requirement "
                    f"{requirement_id} "
                    "sessions must be "
                    "on different days."
                )

        # ----------------------------------------------------
        # 4 CREDIT
        # ----------------------------------------------------

        elif credit_hours == 4:

            if len(values) != 2:

                raise RuntimeError(
                    "Validation failed: "
                    f"requirement "
                    f"{requirement_id} "
                    "must have exactly "
                    "two sessions."
                )

            if durations != [2, 2]:

                raise RuntimeError(
                    "Validation failed: "
                    f"requirement "
                    f"{requirement_id} "
                    "must have two "
                    "2-hour sessions."
                )

            if len(days_for_requirement) != 2:

                raise RuntimeError(
                    "Validation failed: "
                    f"requirement "
                    f"{requirement_id} "
                    "sessions must be "
                    "on different days."
                )

        else:

            raise RuntimeError(
                "Validation failed: "
                f"unsupported credit hours "
                f"{credit_hours} for "
                f"requirement "
                f"{requirement_id}."
            )

    # ========================================================
    # CHECK LECTURER CONFLICTS
    # ========================================================

    lecturer_sessions = defaultdict(list)

    for session in sessions:

        lecturer_sessions[
            session["lecturer_id"]
        ].append(session)

    # ========================================================
    # CHECK SECTION CONFLICTS
    # ========================================================

    section_sessions = defaultdict(list)

    for session in sessions:

        section_sessions[
            session[
                "student_section_id"
            ]
        ].append(session)

    # ========================================================
    # GENERIC OVERLAP CHECKING
    # ========================================================

    def check_resource(
        resource_sessions,
        resource_name
    ):

        for resource_id, values in (
            resource_sessions.items()
        ):

            for i in range(
                len(values)
            ):

                for j in range(
                    i + 1,
                    len(values)
                ):

                    first = values[i]
                    second = values[j]

                    if (
                        first["day"]
                        !=
                        second["day"]
                    ):
                        continue

                    first_start = (
                        time_to_minutes(
                            first["start_time"]
                        )
                    )

                    first_end = (
                        time_to_minutes(
                            first["end_time"]
                        )
                    )

                    second_start = (
                        time_to_minutes(
                            second["start_time"]
                        )
                    )

                    second_end = (
                        time_to_minutes(
                            second["end_time"]
                        )
                    )

                    if (
                        first_start
                        <
                        second_end
                        and
                        second_start
                        <
                        first_end
                    ):

                        raise RuntimeError(
                            "Validation failed: "
                            f"{resource_name} "
                            f"{resource_id} "
                            "has overlapping "
                            "sessions."
                        )

    # ========================================================
    # LECTURER
    # ========================================================

    check_resource(
        lecturer_sessions,
        "Lecturer"
    )

    # ========================================================
    # STUDENT SECTION
    # ========================================================

    check_resource(
        section_sessions,
        "Student section"
    )

    # ========================================================
    # ROOM
    # ========================================================

    room_sessions = defaultdict(list)

    for session in sessions:

        room_sessions[
            session["room_id"]
        ].append(session)

        if (
            session["room_capacity"]
            <
            session["student_count"]
        ):

            raise RuntimeError(
                "Validation failed: "
                "room capacity is "
                "too small."
            )

    check_resource(
        room_sessions,
        "Room"
    )

    return True


# ============================================================
# CREATE SCHEDULE
# ============================================================

def create_schedule():
    """
    Main function called by the FastAPI API.
    """

    print()
    print("=" * 70)
    print(
        "QINBIR COMPACT UNIVERSITY SCHEDULER"
    )
    print("=" * 70)

    # ========================================================
    # LOAD DATA
    # ========================================================

    print()
    print(
        "Loading database data..."
    )

    data = load_data()

    requirements = data[
        "requirements"
    ]

    rooms = data[
        "rooms"
    ]

    time_slots = data[
        "time_slots"
    ]

    availability = data[
        "availability"
    ]

    print()
    print("DATA LOADED")
    print("-" * 70)

    print(
        f"Requirements:         "
        f"{len(requirements):,}"
    )

    print(
        f"Rooms:                "
        f"{len(rooms):,}"
    )

    print(
        f"Time slots:           "
        f"{len(time_slots):,}"
    )

    print(
        f"Availability records: "
        f"{len(availability):,}"
    )

    if not requirements:

        raise RuntimeError(
            "No course requirements found."
        )

    if not rooms:

        raise RuntimeError(
            "No rooms found."
        )

    if not time_slots:

        raise RuntimeError(
            "No time slots found."
        )

    # ========================================================
    # CREDIT DISTRIBUTION
    # ========================================================

    credit_distribution = defaultdict(int)

    for requirement in requirements:

        credit_hours = int(
            requirement[
                "credit_hours"
            ]
        )

        credit_distribution[
            credit_hours
        ] += 1

    print()
    print(
        "CREDIT-HOUR DISTRIBUTION"
    )
    print("-" * 70)

    for credit_hours in sorted(
        credit_distribution
    ):

        print(
            f"{credit_hours} credits: "
            f"{credit_distribution[credit_hours]:,} "
            "requirements"
        )

    # ========================================================
    # SLOT GROUPS
    # ========================================================

    long_slots, short_slots = (
        build_slot_groups(
            time_slots
        )
    )

    print()
    print(
        "TIME SLOT GROUPS"
    )
    print("-" * 70)

    print(
        f"2-hour slots: "
        f"{len(long_slots)}"
    )

    print(
        f"1-hour slots: "
        f"{len(short_slots)}"
    )

    # ========================================================
    # CANDIDATES
    # ========================================================

    print()
    print(
        "BUILDING TIME CANDIDATES..."
    )

    (
        long_candidates,
        short_candidates
    ) = build_candidates(
        requirements,
        long_slots,
        short_slots,
        availability,
    )

    print()
    print(
        "TIME CANDIDATES"
    )
    print("-" * 70)

    print(
        f"2-hour candidates: "
        f"{len(long_candidates):,}"
    )

    print(
        f"1-hour candidates: "
        f"{len(short_candidates):,}"
    )

    # ========================================================
    # MAKE SURE REQUIRED CANDIDATES EXIST
    # ========================================================

    long_requirement_ids = {
        candidate[0]
        for candidate in long_candidates
    }

    short_requirement_ids = {
        candidate[0]
        for candidate in short_candidates
    }

    # --------------------------------------------------------
    # Long session required for:
    #
    # 2 credits
    # 3 credits
    # 4 credits
    # --------------------------------------------------------

    missing_long = [
        requirement["id"]
        for requirement in requirements
        if int(
            requirement["credit_hours"]
        ) in (2, 3, 4)
        and requirement["id"]
        not in long_requirement_ids
    ]

    # --------------------------------------------------------
    # Short session required ONLY for:
    #
    # 3 credits
    # --------------------------------------------------------

    missing_short = [
        requirement["id"]
        for requirement in requirements
        if int(
            requirement["credit_hours"]
        ) == 3
        and requirement["id"]
        not in short_requirement_ids
    ]

    if missing_long:

        raise RuntimeError(
            "No feasible 2-hour slot "
            "for requirements: "
            f"{missing_long[:20]}"
        )

    if missing_short:

        raise RuntimeError(
            "No feasible 1-hour slot "
            "for 3-credit requirements: "
            f"{missing_short[:20]}"
        )

    # ========================================================
    # BUILD MODEL
    # ========================================================

    print()
    print(
        "BUILDING COMPACT CBC MODEL..."
    )

    (
        model,
        long_vars,
        short_vars,
    ) = build_model(
        requirements,
        time_slots,
        long_candidates,
        short_candidates,
    )

    # ========================================================
    # SOLVE
    # ========================================================

    solve_model(model)

    status = LpStatus[
        model.status
    ]

    if status != "Optimal":

        raise RuntimeError(
            "Scheduler failed.\n"
            f"CBC status: {status}"
        )

    # ========================================================
    # EXTRACT TIME SOLUTION
    # ========================================================

    print()
    print(
        "CBC SOLUTION FOUND"
    )

    sessions = extract_sessions(
        requirements,
        time_slots,
        long_vars,
        short_vars,
    )

    print(
        f"Sessions selected: "
        f"{len(sessions):,}"
    )

    # ========================================================
    # ROOM ASSIGNMENT
    # ========================================================

    print()
    print(
        "ASSIGNING ROOMS..."
    )

    sessions = assign_rooms(
        sessions,
        rooms,
        time_slots,
    )

    print(
        f"Rooms assigned: "
        f"{len(sessions):,}"
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    print()
    print(
        "VALIDATING SCHEDULE..."
    )

    validate_schedule(
        sessions
    )

    print(
        "Validation: PASS"
    )

    # ========================================================
    # SAVE
    # ========================================================

    print()
    print(
        "SAVING SCHEDULE..."
    )

    (
        schedule_id,
        entry_count
    ) = save_schedule(
        sessions
    )

    # ========================================================
    # COMPLETE
    # ========================================================

    print()
    print("=" * 70)
    print(
        "QINBIR SCHEDULER COMPLETE"
    )
    print("=" * 70)

    print(
        "Status:       SUCCESS"
    )

    print(
        "Schedule ID:  ",
        schedule_id
    )

    print(
        "Entries:      ",
        entry_count
    )

    return {
        "schedule_id": schedule_id,
        "status": "SUCCESS",
        "entries": entry_count,
    }


# ============================================================
# COMMAND LINE
# ============================================================

def main():
    return create_schedule()


if __name__ == "__main__":
    main()