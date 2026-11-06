"""
validators.py
Input validation helpers (R7).
Author: Student
"""

import re


def validate_email(email: str) -> bool:
    """Return True if the string matches a basic email pattern."""
    pattern = r"^[\w.\-+]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def validate_non_empty(value: str, field_name: str = "Field") -> str:
    """Strip whitespace and raise ValueError if the result is empty."""
    stripped = value.strip()
    if not stripped:
        raise ValueError(f"{field_name} cannot be empty.")
    return stripped


def validate_integer(value: str, field_name: str = "Value", minimum: int = 1) -> int:
    """Convert to int and enforce minimum value."""
    try:
        result = int(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a whole number.")
    if result < minimum:
        raise ValueError(f"{field_name} must be at least {minimum}.")
    return result


def validate_grade(grade: str) -> str | None:
    """Validate that a grade is one of A, B, C, D, F, or blank (None)."""
    grade = grade.strip().upper()
    if grade == "":
        return None
    if grade not in ("A", "B", "C", "D", "F"):
        raise ValueError("Grade must be A, B, C, D, or F (leave blank to skip).")
    return grade


def validate_date(date_str: str) -> str:
    """Ensure date is in YYYY-MM-DD format."""
    import datetime
    date_str = date_str.strip()
    if date_str == "":
        return ""
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")
    return date_str


def safe_input(prompt: str, validator=None, allow_blank: bool = False) -> str:
    """
    Repeatedly prompt the user until valid input is received (R9).
    If validator raises ValueError, show the message and retry.
    """
    while True:
        try:
            value = input(prompt).strip()
            if not value and allow_blank:
                return value
            if validator:
                return validator(value)
            return value
        except ValueError as err:
            print(f"  [!] {err} Please try again.")
