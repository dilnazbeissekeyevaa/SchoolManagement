"""
course.py
Course entity model – inherits from BaseModel.
Author: Student
"""

from models.base_model import BaseModel
from database.db_manager import get_connection


class Course(BaseModel):
    """Represents a course record."""

    TABLE_NAME = "Courses"
    PRIMARY_KEY = "course_id"
    FIELDS = ["course_name", "course_code", "credits", "teacher_id"]

    def __init__(
        self,
        course_name: str,
        course_code: str,
        credits: int = 3,
        teacher_id: int = None,
        course_id: int = None,
    ):
        self._course_id = course_id
        self._course_name = course_name.strip()
        self._course_code = course_code.strip().upper()
        self._credits = int(credits)
        self._teacher_id = teacher_id

    @property
    def course_id(self):
        return self._course_id

    def save(self) -> int:
        sql = """
            INSERT INTO Courses (course_name, course_code, credits, teacher_id)
            VALUES (?, ?, ?, ?);
        """
        row_id = self._execute(sql, (
            self._course_name, self._course_code, self._credits, self._teacher_id
        ))
        self._course_id = row_id
        return row_id

    def update(self) -> bool:
        sql = """
            UPDATE Courses
            SET course_name = ?, course_code = ?, credits = ?, teacher_id = ?
            WHERE course_id = ?;
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (
                self._course_name, self._course_code,
                self._credits, self._teacher_id, self._course_id
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @classmethod
    def get_courses_with_teacher(cls) -> list:
        """JOIN query: returns courses with their assigned teacher names (O3)."""
        sql = """
            SELECT
                c.course_id,
                c.course_name,
                c.course_code,
                c.credits,
                t.first_name || ' ' || t.last_name AS teacher_name,
                t.department
            FROM Courses c
            LEFT JOIN Teachers t ON c.teacher_id = t.teacher_id
            ORDER BY c.course_id;
        """
        return cls._query(sql)

    def __str__(self) -> str:
        return (
            f"Course [ID={self._course_id}] {self._course_name} "
            f"({self._course_code}) | Credits: {self._credits}"
        )
