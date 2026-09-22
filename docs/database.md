# QINBIR Database

QINBIR uses SQLite for local development.

SQLite provides a lightweight database without requiring a separate
database server.

SQLAlchemy is used as the database abstraction layer so that the application
can later migrate to PostgreSQL if required.

## Database File

The local database is:

qinbir.db

## Development Architecture

React → FastAPI → SQLAlchemy → SQLite