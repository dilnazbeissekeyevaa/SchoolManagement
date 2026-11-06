"""
teacher_ui.py
CLI menu for Teacher CRUD operations.
Author: Student
"""

from models.teacher import Teacher
from utils.display import print_header, print_success, print_error, print_table
from utils.validators import validate_non_empty, validate_email, safe_input


def _email_validator(value: str) -> str:
    value = validate_non_empty(value, "Email")
    if not validate_email(value):
        raise ValueError("Invalid email address format.")
    return value


def _get_teacher_or_error(tid: str) -> dict | None:
    try:
        pk = int(tid)
    except ValueError:
        print_error("ID must be a number.")
        return None
    record = Teacher.get_by_id(pk)
    if not record:
        print_error(f"No teacher found with ID {pk}.")
    return record


def add_teacher() -> None:
    print_header("Add New Teacher")
    try:
        first = safe_input("  First name  : ", lambda v: validate_non_empty(v, "First name"))
        last  = safe_input("  Last name   : ", lambda v: validate_non_empty(v, "Last name"))
        email = safe_input("  Email       : ", _email_validator)
        dept  = safe_input("  Department  : ", lambda v: validate_non_empty(v, "Department"))

        teacher = Teacher(first, last, email, dept)
        teacher.save()
        print_success(f"Teacher '{teacher.full_name}' added (ID={teacher.teacher_id}).")
    except KeyboardInterrupt:
        print("\n  Cancelled.")


def view_all_teachers() -> None:
    print_header("All Teachers")
    print_table(Teacher.get_all(), title="Teachers")


def update_teacher() -> None:
    print_header("Update Teacher")
    tid = input("  Enter teacher ID to update: ").strip()
    record = _get_teacher_or_error(tid)
    if not record:
        return
    try:
        first = safe_input("  New first name  (Enter to keep): ",
                           lambda v: validate_non_empty(v, "First name"),
                           allow_blank=True) or record["first_name"]
        last  = safe_input("  New last name   (Enter to keep): ",
                           lambda v: validate_non_empty(v, "Last name"),
                           allow_blank=True) or record["last_name"]
        email = safe_input("  New email       (Enter to keep): ",
                           _email_validator, allow_blank=True) or record["email"]
        dept  = safe_input("  New department  (Enter to keep): ",
                           lambda v: validate_non_empty(v, "Department"),
                           allow_blank=True) or record["department"]

        teacher = Teacher(first, last, email, dept, teacher_id=record["teacher_id"])
        if teacher.update():
            print_success("Teacher updated.")
        else:
            print_error("Update failed.")
    except KeyboardInterrupt:
        print("\n  Cancelled.")


def delete_teacher() -> None:
    print_header("Delete Teacher")
    tid = input("  Enter teacher ID to delete: ").strip()
    record = _get_teacher_or_error(tid)
    if not record:
        return
    confirm = input(
        f"  Delete '{record['first_name']} {record['last_name']}'? (yes/no): "
    ).strip().lower()
    if confirm != "yes":
        print("  Cancelled.")
        return
    if Teacher.delete_by_id(record["teacher_id"]):
        print_success("Teacher deleted.")
    else:
        print_error("Deletion failed.")


def search_teachers() -> None:
    print_header("Search Teachers")
    print("  Search by: 1) First name  2) Last name  3) Email  4) Department")
    field_map = {"1": "first_name", "2": "last_name", "3": "email", "4": "department"}
    choice = input("  Choice: ").strip()
    field = field_map.get(choice)
    if not field:
        print_error("Invalid choice.")
        return
    term = input("  Search term: ").strip()
    results = Teacher.search(field, term)
    print_table(results, title=f"Search Results ({len(results)} found)")


def teacher_menu() -> None:
    options = {
        "1": ("Add teacher",       add_teacher),
        "2": ("View all teachers", view_all_teachers),
        "3": ("Update teacher",    update_teacher),
        "4": ("Delete teacher",    delete_teacher),
        "5": ("Search teachers",   search_teachers),
        "0": ("Back",              None),
    }

    while True:
        print_header("Teacher Management")
        for key, (label, _) in options.items():
            print(f"   [{key}] {label}")
        choice = input("\n  Enter choice: ").strip()
        if choice == "0":
            break
        action = options.get(choice)
        if action:
            try:
                action[1]()
            except Exception as err:
                print_error(f"Unexpected error: {err}")
        else:
            print_error("Invalid option.")
