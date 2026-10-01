# ቅንብር — QINBIR


Smart University Timetable Scheduling System.

QINBIR is a university scheduling platform designed to generate valid
and conflict-free academic timetables using constraint-based scheduling.

## Features

- University department management
- Program management
- Course management
- Lecturer management
- Student section management
- Room management
- Time-slot management
- Lecturer availability management
- Course requirement management
- Scheduling constraints
- Automatic timetable generation
- Schedule and timetable viewing
- Schedule entry management

## Scheduling Engine

QINBIR uses a constraint-based optimization engine built with Python
and PuLP/CBC.

The scheduler considers:

- Course requirements
- Credit hours
- Lecturer availability
- Student-section conflicts
- Lecturer conflicts
- Room conflicts
- Room capacity
- Time-slot availability

The generated timetable is validated before it is saved to the database.

## Backend

The backend is built with:

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite for local development
- PuLP
- CBC solver

## Frontend

The frontend is built with:

- React
- Vite
- JavaScript
- Axios
- React Router

The frontend provides interfaces for managing university data,
generating schedules, and viewing generated timetables.

## Database

SQLite is used for local development.

SQLAlchemy provides the database abstraction layer so that QINBIR can
later migrate to PostgreSQL if needed.

## Deployment

- Docker
- Docker Compose

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