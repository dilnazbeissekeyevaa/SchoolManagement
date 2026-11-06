"""
student.py
Student entity model – inherits from BaseModel.
Author: Student
"""

from models.base_model import BaseModel
from database.db_manager import get_connection


class Student(BaseModel):
    """Represents a student record."""

    TABLE_NAME = "Students"
    PRIMARY_KEY = "student_id"
    FIELDS = ["first_name", "last_name", "email", "date_of_birth", "enroll_date"]

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        date_of_birth: str = "",
        enroll_date: str = "",
        student_id: int = None,
    ):
        # Encapsulation: private-style attributes via name convention
        self._student_id = student_id
        self._first_name = first_name.strip()
        self._last_name = last_name.strip()
        self._email = email.strip()
        self._date_of_birth = date_of_birth
        self._enroll_date = enroll_date

    # -------------------- properties ----------------------------------- #
    @property
    def student_id(self):
        return self._student_id

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    # -------------------- CRUD ----------------------------------------- #
    def save(self) -> int:
        """INSERT a new student into the database."""
        sql = """
            INSERT INTO Students (first_name, last_name, email, date_of_birth)
            VALUES (?, ?, ?, ?);
        """
        row_id = self._execute(sql, (
            self._first_name, self._last_name, self._email, self._date_of_birth
        ))
        self._student_id = row_id
        return row_id

    def update(self) -> bool:
        """UPDATE an existing student record."""
        sql = """
            UPDATE Students
            SET first_name = ?, last_name = ?, email = ?, date_of_birth = ?
            WHERE student_id = ?;
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (
                self._first_name, self._last_name,
                self._email, self._date_of_birth, self._student_id
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    # -------------------- extra reports (O3) --------------------------- #
    @classmethod
    def get_students_with_courses(cls) -> list:
        """
        JOIN query returning each student with their enrolled courses.
        Uses SQL JOIN across Students, Registrations, and Courses (O3).
        """
        sql = """
            SELECT
                s.student_id,
                s.first_name || ' ' || s.last_name AS student_name,
                s.email,
                c.course_name,
                c.course_code,
                r.grade,
                r.registration_date
            FROM Students s
            LEFT JOIN Registrations r ON s.student_id = r.student_id
            LEFT JOIN Courses       c ON r.course_id  = c.course_id
            ORDER BY s.last_name, s.first_name;
        """
        return cls._query(sql)

    def __str__(self) -> str:
        return (
            f"Student [ID={self._student_id}] {self.full_name} "
            f"| Email: {self._email} | DOB: {self._date_of_birth}"
        )
