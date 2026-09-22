# ቅንብር — QINBIR

## Smart University Course Scheduling System

QINBIR is a web-based university course scheduling system that automatically
generates timetables based on courses, lecturers, classrooms, student sections,
available time slots, and scheduling constraints.

## Project Goal

The goal of QINBIR is to reduce manual timetable creation and minimize
scheduling conflicts.

## Technology Stack

<<<<<<< Updated upstream
- Frontend: React
- Backend: FastAPI
- Database: SQLite
- Scheduling Engine: Python + OR-Tools
- Authentication: JWT
- Deployment: Docker
=======
### Frontend
>>>>>>> Stashed changes

- React
- Vite
- Axios
- React Router

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite

### Scheduling Engine

- Python
- Google OR-Tools

### Deployment

- Docker
- Docker Compose

## Database

SQLite is used for local development.

SQLAlchemy provides the database abstraction layer so that QINBIR can
later migrate to PostgreSQL if needed.

## Project Structure

```text
QINBIR/
├── backend/
├── frontend/
├── scheduler/
├── docs/
├── tests/
├── docker-compose.yml
└── README.md