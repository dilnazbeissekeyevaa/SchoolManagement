#registration.py
#Registration entity model – inherits from BaseModel.
#Author: Student


from models.base_model import BaseModel
from database.db_manager import get_connection


class Registration(BaseModel):
#Represents a student-course registration record.

    TABLE_NAME = "Registrations"
    PRIMARY_KEY = "registration_id"
    FIELDS = ["student_id", "course_id", "registration_date", "grade"]

    def __init__(
        self,
        student_id: int,
        course_id: int,
        grade: str = None,
        registration_date: str = "",
        registration_id: int = None,
    ):
        self._registration_id = registration_id
        self._student_id = student_id
        self._course_id = course_id
        self._grade = grade
        self._registration_date = registration_date

    @property
    def registration_id(self):
        return self._registration_id

    def save(self) -> int:
        sql = """
            INSERT INTO Registrations (student_id, course_id, grade)
            VALUES (?, ?, ?);
        """
        row_id = self._execute(sql, (self._student_id, self._course_id, self._grade))
        self._registration_id = row_id
        return row_id

    def update(self) -> bool:
        """Update the grade for this registration."""
        sql = "UPDATE Registrations SET grade = ? WHERE registration_id = ?;"
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (self._grade, self._registration_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @classmethod
    def get_full_report(cls) -> list:
        
#Full JOIN across all four core tables to produce a registration report.
#Demonstrates multi-table JOIN (O3).
        
        sql = """
            SELECT
                r.registration_id,
                s.student_id,
                s.first_name || ' ' || s.last_name  AS student_name,
                c.course_name,
                c.course_code,
                t.first_name || ' ' || t.last_name  AS teacher_name,
                r.registration_date,
                r.grade
            FROM Registrations r
            JOIN Students  s ON r.student_id = s.student_id
            JOIN Courses   c ON r.course_id  = c.course_id
            LEFT JOIN Teachers t ON c.teacher_id = t.teacher_id
            ORDER BY r.registration_id;
        """
        return cls._query(sql)

    def __str__(self) -> str:
        return (
            f"Registration [ID={self._registration_id}] "
            f"Student={self._student_id} Course={self._course_id} "
            f"Grade={self._grade}"
        )
