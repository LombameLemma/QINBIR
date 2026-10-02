from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base

# ============================================================
# IMPORT ALL MODELS
# ============================================================
# Importing the models ensures SQLAlchemy knows about all
# database tables before create_all() is called.

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
    departments,
    programs,
    courses,
    lecturers,
    users,
    student_sections,
    rooms,
    time_slots,
    course_requirements,
    lecturer_availability,
    schedules,
    schedule_entries,
    constraints,
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

# Local development URLs
# Production Vercel URL will be added when the final
# Vercel domain is confirmed.

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"https://qinbir-.*-lombamelemma-3566s-projects\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API ROUTES
# ============================================================

app.include_router(departments.router)
app.include_router(programs.router)
app.include_router(courses.router)
app.include_router(lecturers.router)
app.include_router(users.router)
app.include_router(student_sections.router)
app.include_router(rooms.router)
app.include_router(time_slots.router)
app.include_router(course_requirements.router)
app.include_router(lecturer_availability.router)
app.include_router(schedules.router)
app.include_router(schedule_entries.router)
app.include_router(constraints.router)


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