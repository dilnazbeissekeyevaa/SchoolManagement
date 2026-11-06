"""
seed.py
Populates the School Management System database using real names from sex.csv.
Place this file in the project root (next to main.py) and run:  python seed.py

CSV expected at:  sex.csv  (in the same folder as seed.py)
"""

import sqlite3
import os
import csv
import random
from datetime import datetime

DB_PATH  = os.path.join(os.path.dirname(__file__), "database", "school.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "sex.csv")

DEPARTMENTS = [
    "Computer Science", "Mathematics", "Physics",
    "English", "History", "Biology"
]

COURSES = [
    ("Introduction to Programming", "CS101", 3),
    ("Database Systems",            "CS201", 4),
    ("Web Development",             "CS301", 3),
    ("Mathematics I",               "MT101", 4),
    ("Mathematics II",              "MT201", 4),
    ("English Composition",         "EN101", 3),
    ("Physics I",                   "PH101", 4),
    ("Data Structures",             "CS202", 3),
    ("Software Engineering",        "CS401", 4),
    ("History of Science",          "HS101", 3),
]

GRADES    = ["A", "B", "C", "D", "F", None]
STATUSES  = ["Present", "Present", "Present", "Absent", "Late"]


# ── helpers ──────────────────────────────────────────────────────────────────

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def parse_date(s: str) -> str | None:
    """Convert '06 June 1985' → '1985-06-06', or return None."""
    try:
        return datetime.strptime(s.strip(), "%d %B %Y").strftime("%Y-%m-%d")
    except ValueError:
        return None


def load_people(csv_path: str, n: int = 50) -> list[dict]:
    """Read CSV and return n clean rows (non-empty first/last name)."""
    with open(csv_path, encoding="latin-1") as f:
        rows = list(csv.DictReader(f))
    clean = [r for r in rows if r["firstName"].strip() and r["lastName"].strip()]
    return random.sample(clean, min(n, len(clean)))


# ── main seed ────────────────────────────────────────────────────────────────

def seed():
    people = load_people(CSV_PATH, 50)   # 10 teachers + 40 students
    teachers_data = people[:10]
    students_data = people[10:]

    conn = get_connection()
    cur  = conn.cursor()

    # ── 1. Teachers (10) ─────────────────────────────────────────────────────
    print("Inserting teachers...")
    for p in teachers_data:
        cur.execute(
            "INSERT OR IGNORE INTO Teachers "
            "(first_name, last_name, email, department) VALUES (?,?,?,?);",
            (
                p["firstName"].strip(),
                p["lastName"].strip(),
                p["email"].strip(),
                random.choice(DEPARTMENTS),
            ),
        )
    conn.commit()

    teacher_ids = [r[0] for r in cur.execute("SELECT teacher_id FROM Teachers;")]
    print(f"  → {len(teacher_ids)} teachers")

    # ── 2. Courses (10) ──────────────────────────────────────────────────────
    print("Inserting courses...")
    for name, code, credits in COURSES:
        cur.execute(
            "INSERT OR IGNORE INTO Courses "
            "(course_name, course_code, credits, teacher_id) VALUES (?,?,?,?);",
            (name, code, credits, random.choice(teacher_ids)),
        )
    conn.commit()

    course_ids = [r[0] for r in cur.execute("SELECT course_id FROM Courses;")]
    print(f"  → {len(course_ids)} courses")

    # ── 3. Students (40) ─────────────────────────────────────────────────────
    print("Inserting students...")
    for p in students_data:
        cur.execute(
            "INSERT OR IGNORE INTO Students "
            "(first_name, last_name, email, date_of_birth) VALUES (?,?,?,?);",
            (
                p["firstName"].strip(),
                p["lastName"].strip(),
                p["email"].strip(),
                parse_date(p["Birthdate"]),
            ),
        )
    conn.commit()

    student_ids = [r[0] for r in cur.execute("SELECT student_id FROM Students;")]
    print(f"  → {len(student_ids)} students")

    # ── 4. Registrations (2-3 courses per student) ───────────────────────────
    print("Inserting registrations...")
    reg_count = 0
    for sid in student_ids:
        for cid in random.sample(course_ids, k=min(random.randint(2, 3), len(course_ids))):
            cur.execute(
                "INSERT OR IGNORE INTO Registrations "
                "(student_id, course_id, grade) VALUES (?,?,?);",
                (sid, cid, random.choice(GRADES)),
            )
            reg_count += 1
    conn.commit()
    print(f"  → {reg_count} registrations")

    # ── 5. Attendance (sample) ───────────────────────────────────────────────
    print("Inserting attendance...")
    att_count = 0
    sample_dates = [
        f"2026-0{m}-{d:02d}"
        for m in range(1, 6)
        for d in random.sample(range(1, 28), 2)
    ]
    for sid in random.sample(student_ids, k=min(20, len(student_ids))):
        for cid in random.sample(course_ids, k=2):
            for date in random.sample(sample_dates, k=3):
                cur.execute(
                    "INSERT OR IGNORE INTO Attendance "
                    "(student_id, course_id, attend_date, status) VALUES (?,?,?,?);",
                    (sid, cid, date, random.choice(STATUSES)),
                )
                att_count += 1
    conn.commit()
    print(f"  → {att_count} attendance records")

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n✅ Seed complete!")
    for table in ("Students", "Teachers", "Courses", "Registrations", "Attendance"):
        count = cur.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
        print(f"   {table:<15} {count}")

    conn.close()


if __name__ == "__main__":
    seed()
