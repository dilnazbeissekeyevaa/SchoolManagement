"""
student_ui.py
CLI menu for Student CRUD operations (R4, R5, R6, R7, R9).
Author: Student
"""

from models.student import Student
from utils.display import print_header, print_success, print_error, print_table
from utils.validators import validate_non_empty, validate_email, validate_date, safe_input


def _get_student_or_error(sid: str) -> dict | None:
    """Helper: fetch student by ID and print an error if not found."""
    try:
        pk = int(sid)
    except ValueError:
        print_error("ID must be a number.")
        return None
    record = Student.get_by_id(pk)
    if not record:
        print_error(f"No student found with ID {pk}.")
    return record


def add_student() -> None:
    """Prompt for details and INSERT a new student."""
    print_header("Add New Student")
    try:
        first = safe_input("  First name : ", lambda v: validate_non_empty(v, "First name"))
        last  = safe_input("  Last name  : ", lambda v: validate_non_empty(v, "Last name"))
        email = safe_input("  Email      : ", lambda v: _email_validator(v))
        dob   = safe_input("  Date of Birth (YYYY-MM-DD, or press Enter to skip): ",
                           validate_date, allow_blank=True)

        student = Student(first, last, email, dob)
        student.save()
        print_success(f"Student '{student.full_name}' added (ID={student.student_id}).")
    except KeyboardInterrupt:
        print("\n  Cancelled.")


def _email_validator(value: str) -> str:
    value = validate_non_empty(value, "Email")
    if not validate_email(value):
        raise ValueError("Invalid email address format.")
    return value


def view_all_students() -> None:
    """Display all students in a formatted table."""
    print_header("All Students")
    records = Student.get_all()
    print_table(records, title="Students")


def update_student() -> None:
    """Update an existing student record."""
    print_header("Update Student")
    sid = input("  Enter student ID to update: ").strip()
    record = _get_student_or_error(sid)
    if not record:
        return

    print(f"  Current: {record['first_name']} {record['last_name']} | {record['email']}")
    try:
        first = safe_input("  New first name (Enter to keep): ",
                           lambda v: validate_non_empty(v, "First name"),
                           allow_blank=True) or record["first_name"]
        last  = safe_input("  New last name  (Enter to keep): ",
                           lambda v: validate_non_empty(v, "Last name"),
                           allow_blank=True) or record["last_name"]
        email = safe_input("  New email      (Enter to keep): ",
                           lambda v: _email_validator(v),
                           allow_blank=True) or record["email"]
        dob   = safe_input("  New DOB YYYY-MM-DD (Enter to keep): ",
                           validate_date, allow_blank=True) or record["date_of_birth"]

        student = Student(first, last, email, dob, student_id=record["student_id"])
        if student.update():
            print_success("Student updated successfully.")
        else:
            print_error("Update failed – no rows affected.")
    except KeyboardInterrupt:
        print("\n  Cancelled.")


def delete_student() -> None:
    """Delete a student by ID."""
    print_header("Delete Student")
    sid = input("  Enter student ID to delete: ").strip()
    record = _get_student_or_error(sid)
    if not record:
        return

    confirm = input(
        f"  Delete '{record['first_name']} {record['last_name']}'? (yes/no): "
    ).strip().lower()
    if confirm != "yes":
        print("  Deletion cancelled.")
        return

    if Student.delete_by_id(record["student_id"]):
        print_success("Student deleted.")
    else:
        print_error("Deletion failed.")


def search_students() -> None:
    """Search students by name or email (R5)."""
    print_header("Search Students")
    print("  Search by: 1) First name  2) Last name  3) Email  4) Student ID")
    choice = input("  Choice: ").strip()
    field_map = {"1": "first_name", "2": "last_name", "3": "email", "4": "student_id"}
    field = field_map.get(choice)
    if not field:
        print_error("Invalid choice.")
        return
    term = input(f"  Enter search term: ").strip()
    results = Student.search(field, term)
    print_table(results, title=f"Search Results ({len(results)} found)")


def sort_students() -> None:
    """Sort and display students (R5)."""
    print_header("Sort Students")
    print("  Sort by: 1) Last name  2) First name  3) Email  4) Enrol date")
    choice = input("  Choice: ").strip()
    field_map = {
        "1": "last_name", "2": "first_name",
        "3": "email",    "4": "enroll_date"
    }
    field = field_map.get(choice, "last_name")
    order = input("  Order (1=ASC, 2=DESC): ").strip()
    ascending = order != "2"
    results = Student.sort_by(field, ascending)
    print_table(results, title="Sorted Students")


def student_course_report() -> None:
    """Show student-course enrolment report using JOIN (O3)."""
    print_header("Student–Course Enrolment Report")
    rows = Student.get_students_with_courses()
    print_table(rows, title="Enrolment Report")


def student_menu() -> None:
    """Main student management loop (R9)."""
    options = {
        "1": ("Add student",               add_student),
        "2": ("View all students",          view_all_students),
        "3": ("Update student",             update_student),
        "4": ("Delete student",             delete_student),
        "5": ("Search students",            search_students),
        "6": ("Sort students",              sort_students),
        "7": ("Student–course report",      student_course_report),
        "0": ("Back to main menu",          None),
    }

    while True:
        print_header("Student Management")
        for key, (label, _) in options.items():
            print(f"   [{key}] {label}")

        choice = input("\n  Enter choice: ").strip()
        if choice == "0":
            break
        action = options.get(choice)
        if action:
            try:
                action[1]()
            except Exception as err:  # R6 – catch unexpected DB errors
                print_error(f"Unexpected error: {err}")
        else:
            print_error("Invalid option. Please try again.")
