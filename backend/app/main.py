
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.security import require_role

# ============================================================
# IMPORT ALL MODELS
# ============================================================

from app.models.user import User
from app.models.department import Department
from app.models.program import Program
from app.models.course import Course
from app.models.program_course import ProgramCourse
from app.models.lecturer import Lecturer
from app.models.student import Student
from app.models.student_section import StudentSection
from app.models.room import Room
from app.models.time_slot import TimeSlot
from app.models.lecturer_availability import LecturerAvailability
from app.models.course_requirement import CourseRequirement
from app.models.schedule import Schedule
from app.models.schedule_entry import ScheduleEntry
from app.models.constraint import Constraint

# ============================================================
# IMPORT ROUTES
# ============================================================

from app.routes import (
    auth,
    departments,
    programs,
    courses,
    lecturers,
    students,
    student_sections,
    rooms,
    time_slots,
    course_requirements,
    lecturer_availability,
    schedules,
    schedule_entries,
    constraints,
    timetable,
    
)

# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="QINBIR API",
    description="Automatic University Course Scheduling System",
    version="1.0.0",
)

# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
   allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://qinbir-tt4t.vercel.app",
],
    allow_origin_regex=r"https://qinbir-.*-lombamelemma-3566s-projects\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# API ROUTES
# ============================================================

# Authentication remains available without Admin authorization.
app.include_router(auth.router)

# All existing management APIs require an authenticated Admin.
admin_only = [Depends(require_role("ADMIN"))]

app.include_router(departments.router, dependencies=admin_only)
app.include_router(programs.router, dependencies=admin_only)
app.include_router(courses.router, dependencies=admin_only)
app.include_router(lecturers.router, dependencies=admin_only)
app.include_router(students.router)
app.include_router(student_sections.router, dependencies=admin_only)
app.include_router(rooms.router, dependencies=admin_only)
app.include_router(time_slots.router, dependencies=admin_only)
app.include_router(course_requirements.router, dependencies=admin_only)
app.include_router(lecturer_availability.router, dependencies=admin_only)
app.include_router(schedules.router, dependencies=admin_only)
app.include_router(schedule_entries.router, dependencies=admin_only)
app.include_router(constraints.router, dependencies=admin_only)
app.include_router(timetable.router)

# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "QINBIR API is running"
    }

# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
