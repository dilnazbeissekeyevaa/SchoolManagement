"""
teacher.py
Teacher entity model – inherits from BaseModel.
Author: Student
"""

from models.base_model import BaseModel
from database.db_manager import get_connection


class Teacher(BaseModel):
    """Represents a teacher record."""

    TABLE_NAME = "Teachers"
    PRIMARY_KEY = "teacher_id"
    FIELDS = ["first_name", "last_name", "email", "department"]

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        department: str = "General",
        teacher_id: int = None,
    ):
        self._teacher_id = teacher_id
        self._first_name = first_name.strip()
        self._last_name = last_name.strip()
        self._email = email.strip()
        self._department = department.strip()

    @property
    def teacher_id(self):
        return self._teacher_id

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    def save(self) -> int:
        sql = """
            INSERT INTO Teachers (first_name, last_name, email, department)
            VALUES (?, ?, ?, ?);
        """
        row_id = self._execute(sql, (
            self._first_name, self._last_name, self._email, self._department
        ))
        self._teacher_id = row_id
        return row_id

    def update(self) -> bool:
        sql = """
            UPDATE Teachers
            SET first_name = ?, last_name = ?, email = ?, department = ?
            WHERE teacher_id = ?;
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (
                self._first_name, self._last_name,
                self._email, self._department, self._teacher_id
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def __str__(self) -> str:
        return (
            f"Teacher [ID={self._teacher_id}] {self.full_name} "
            f"| Email: {self._email} | Dept: {self._department}"
        )
