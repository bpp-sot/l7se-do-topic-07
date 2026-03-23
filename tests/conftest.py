"""
conftest.py
-----------
Pytest fixtures for the StudyTrack test suite.

An isolated temporary SQLite database is created for each test session,
seeded with representative student records, and torn down automatically
when the session ends.  Tests should use the `client` fixture rather
than importing Flask's test client directly.
"""

import os
import sqlite3
import tempfile

import pytest

from app import app as flask_app

# ── Seed data for the test database ────────────────────────────────────────────
SEED_DATA = [
    ('STU001', 'Alice',   'Smith',     'Computer Science',      2),
    ('STU002', 'Bob',     'Smith',     'Software Engineering',  3),
    ('STU003', 'Carol',   'Jones',     'Cybersecurity',         1),
    ('STU004', 'David',   'Jones',     'Computer Science',      2),
    ('STU005', 'Fatima',  'Ahmed',     'Software Engineering',  1),
    ('STU006', 'George',  'Williams',  'Computer Science',      3),
    ('STU007', 'Hannah',  'Brown',     'Cybersecurity',         2),
    ('STU008', 'Ibrahim', 'Patel',     'Software Engineering',  1),
    ('STU009', 'Emma',    "O'Brien",   'Software Engineering',  2),
    ('STU010', 'Sean',    "O'Sullivan",'Computer Science',      3),
]


@pytest.fixture(scope='session')
def app():
    """
    Configure the Flask app for testing and provide a temporary SQLite database
    seeded with student records.  The database file is removed after the session.
    """
    db_fd, db_path = tempfile.mkstemp(suffix='.db')

    flask_app.config.update({
        'TESTING': True,
        'DB_PATH': db_path,
    })

    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE students (
            student_id  TEXT PRIMARY KEY,
            first_name  TEXT NOT NULL,
            last_name   TEXT NOT NULL,
            course      TEXT NOT NULL,
            year        INTEGER NOT NULL
        )
    """)
    conn.executemany(
        "INSERT INTO students VALUES (?,?,?,?,?)", SEED_DATA
    )
    conn.commit()
    conn.close()

    yield flask_app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='session')
def client(app):
    """Return a Flask test client bound to the test-configured app."""
    return app.test_client()
