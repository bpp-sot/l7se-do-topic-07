"""
setup_db.py
-----------
Creates and seeds studytrack.db for local development and manual testing.
Run once before starting the Flask app:

    python setup_db.py
    python app.py
"""

import sqlite3

DB_PATH = 'studytrack.db'

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    student_id  TEXT PRIMARY KEY,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    course      TEXT NOT NULL,
    year        INTEGER NOT NULL
);
"""

SEED_DATA = [
    ('STU001', 'Alice',   'Smith',     'Computer Science',       2),
    ('STU002', 'Bob',     'Smith',     'Software Engineering',   3),
    ('STU003', 'Carol',   'Jones',     'Cybersecurity',          1),
    ('STU004', 'David',   'Jones',     'Computer Science',       2),
    ('STU005', 'Fatima',  'Ahmed',     'Software Engineering',   1),
    ('STU006', 'George',  'Williams',  'Computer Science',       3),
    ('STU007', 'Hannah',  'Brown',     'Cybersecurity',          2),
    ('STU008', 'Ibrahim', 'Patel',     'Software Engineering',   1),
    ('STU009', 'Emma',    "O'Brien",   'Software Engineering',   2),
    ('STU010', 'Sean',    "O'Sullivan",'Computer Science',       3),
]

conn = sqlite3.connect(DB_PATH)
conn.execute(SCHEMA)
conn.executemany(
    "INSERT OR IGNORE INTO students VALUES (?,?,?,?,?)", SEED_DATA
)
conn.commit()
conn.close()
print(f"Database seeded at {DB_PATH} — {len(SEED_DATA)} student records inserted.")
