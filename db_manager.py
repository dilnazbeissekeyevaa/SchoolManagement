"""
db_manager.py
Handles SQLite database connection and table creation for the School Management System.
Author: Student
"""

import sqlite3
import os

# Path to the SQLite database file
DB_PATH = os.path.join(os.path.dirname(__file__), "school.db")


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database with foreign key support enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row  # Allows column access by name
    return conn


def initialise_database() -> None:
    """Create all tables if they do not already exist (DDL)."""
    conn = get_connection()
    cursor = conn.cursor()

    # ------------------------------------------------------------------ #
    # STUDENTS table – 3NF: no transitive dependencies                    #
    # ------------------------------------------------------------------ #
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name   TEXT    NOT NULL CHECK(LENGTH(TRIM(first_name)) > 0),
            last_name    TEXT    NOT NULL CHECK(LENGTH(TRIM(last_name)) > 0),
            email        TEXT    NOT NULL UNIQUE,
            date_of_birth TEXT,
            enroll_date  TEXT    NOT NULL DEFAULT (DATE('now'))
        );
    """)

    # ------------------------------------------------------------------ #
    # TEACHERS table                                                       #
    # ------------------------------------------------------------------ #
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Teachers (
            teacher_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name   TEXT    NOT NULL CHECK(LENGTH(TRIM(first_name)) > 0),
            last_name    TEXT    NOT NULL CHECK(LENGTH(TRIM(last_name)) > 0),
            email        TEXT    NOT NULL UNIQUE,
            department   TEXT    NOT NULL DEFAULT 'General'
        );
    """)

    # ------------------------------------------------------------------ #
    # COURSES table                                                        #
    # ------------------------------------------------------------------ #
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Courses (
            course_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name  TEXT    NOT NULL UNIQUE CHECK(LENGTH(TRIM(course_name)) > 0),
            course_code  TEXT    NOT NULL UNIQUE,
            credits      INTEGER NOT NULL DEFAULT 3 CHECK(credits > 0),
            teacher_id   INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
                ON UPDATE CASCADE ON DELETE SET NULL
        );
    """)

    # ------------------------------------------------------------------ #
    # REGISTRATIONS table – resolves many-to-many Students <-> Courses    #
    # ------------------------------------------------------------------ #
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Registrations (
            registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id      INTEGER NOT NULL,
            course_id       INTEGER NOT NULL,
            registration_date TEXT NOT NULL DEFAULT (DATE('now')),
            grade           TEXT    DEFAULT NULL CHECK(
                                grade IS NULL OR grade IN ('A','B','C','D','F')
                            ),
            UNIQUE(student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (course_id)  REFERENCES Courses(course_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        );
    """)

    # ------------------------------------------------------------------ #
    # ATTENDANCE table (optional extra entity O2)                          #
    # ------------------------------------------------------------------ #
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Attendance (
            attendance_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id      INTEGER NOT NULL,
            course_id       INTEGER NOT NULL,
            attend_date     TEXT    NOT NULL DEFAULT (DATE('now')),
            status          TEXT    NOT NULL DEFAULT 'Present'
                                CHECK(status IN ('Present','Absent','Late')),
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (course_id)  REFERENCES Courses(course_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        );
    """)

    # Performance indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_email ON Students(email);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_courses_code  ON Courses(course_code);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reg_student   ON Registrations(student_id);")

    conn.commit()
    conn.close()
    print("[DB] Database initialised successfully.")
