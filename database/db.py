import sqlite3

DB_NAME = "timetable.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # FACULTY
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        max_hours INTEGER
    )
    """)

    # CLASS (NEW)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS class (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        student_count INTEGER,
        semester TEXT
    )
    """)

    # SUBJECT
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subject (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        faculty_id INTEGER,
        weekly_hours INTEGER
    )
    """)

    # ROOM (UPDATED)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS room (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT,
        capacity INTEGER
    )
    """)

    # TIMETABLE (UPDATED)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timetable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id INTEGER,
        class_id INTEGER,
        subject_id INTEGER,
        faculty_id INTEGER,
        room_id INTEGER,
        day TEXT,
        time_slot TEXT
    )
    """)

    # TIMETABLE RUN (NEW)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timetable_run (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()
