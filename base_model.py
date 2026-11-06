"""
base_model.py
Abstract base class that provides common CRUD utilities for all entity models.
Demonstrates OOP Inheritance and Encapsulation (R2).
Author: Student
"""

from abc import ABC, abstractmethod
from database.db_manager import get_connection


class BaseModel(ABC):
    """
    Abstract base class for all database-backed models.

    Subclasses must implement:
        TABLE_NAME  – name of the underlying SQLite table
        FIELDS      – ordered list of column names (excluding the PK)
        PRIMARY_KEY – name of the primary key column
    """

    TABLE_NAME: str = ""
    FIELDS: list = []
    PRIMARY_KEY: str = ""

    # ------------------------------------------------------------------ #
    # Generic helpers                                                       #
    # ------------------------------------------------------------------ #

    @classmethod
    def _execute(cls, sql: str, params: tuple = ()):
        """Execute a write SQL statement (INSERT / UPDATE / DELETE)."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @classmethod
    def _query(cls, sql: str, params: tuple = ()) -> list:
        """Execute a read SQL statement and return all rows as dicts."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    # ------------------------------------------------------------------ #
    # CRUD operations (R4)                                                  #
    # ------------------------------------------------------------------ #

    @classmethod
    def get_all(cls) -> list:
        """Return every record from the table, sorted by primary key."""
        sql = f"SELECT * FROM {cls.TABLE_NAME} ORDER BY {cls.PRIMARY_KEY};"
        return cls._query(sql)

    @classmethod
    def get_by_id(cls, pk) -> dict | None:
        """Return a single record by primary key, or None if not found."""
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE {cls.PRIMARY_KEY} = ?;"
        rows = cls._query(sql, (pk,))
        return rows[0] if rows else None

    @classmethod
    def delete_by_id(cls, pk) -> bool:
        """Delete a record by primary key. Returns True if a row was removed."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM {cls.TABLE_NAME} WHERE {cls.PRIMARY_KEY} = ?;", (pk,)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    # ------------------------------------------------------------------ #
    # Searching & Sorting (R5)                                              #
    # ------------------------------------------------------------------ #

    @classmethod
    def search(cls, field: str, value: str) -> list:
        """
        Case-insensitive LIKE search on a given field.
        Example: Student.search('last_name', 'smith')
        """
        if field not in cls.FIELDS + [cls.PRIMARY_KEY]:
            raise ValueError(f"Unknown field '{field}' for {cls.TABLE_NAME}.")
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE {field} LIKE ?;"
        return cls._query(sql, (f"%{value}%",))

    @classmethod
    def sort_by(cls, field: str, ascending: bool = True) -> list:
        """Return all records sorted by the given field."""
        if field not in cls.FIELDS + [cls.PRIMARY_KEY]:
            raise ValueError(f"Unknown field '{field}' for {cls.TABLE_NAME}.")
        direction = "ASC" if ascending else "DESC"
        sql = f"SELECT * FROM {cls.TABLE_NAME} ORDER BY {field} {direction};"
        return cls._query(sql)

    # ------------------------------------------------------------------ #
    # Abstract interface                                                    #
    # ------------------------------------------------------------------ #

    @abstractmethod
    def save(self) -> int:
        """Persist (INSERT) this instance to the database."""

    @abstractmethod
    def update(self) -> bool:
        """Update this instance's row in the database."""

    @abstractmethod
    def __str__(self) -> str:
        """Human-readable representation."""
