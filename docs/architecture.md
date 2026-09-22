# QINBIR Architecture

QINBIR consists of three main application components:

1. React frontend
2. FastAPI backend
3. Python scheduling engine

SQLite is used as the primary database for local development.

SQLAlchemy provides the database abstraction layer.

## Application Flow

React Frontend
       ↓
FastAPI Backend
       ↓
SQLAlchemy
       ↓
SQLite Database