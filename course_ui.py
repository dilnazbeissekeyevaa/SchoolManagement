"""
course_ui.py
CLI menu for Course CRUD operations.
Author: Student
"""

from models.course import Course
from utils.display import print_header, print_success, print_error, print_table
from utils.validators import validate_non_empty, validate_integer, safe_input


def _get_course_or_error(cid: str) -> dict | None:
    try:
        pk = int(cid)
    except ValueError:
        print_error("ID must be a number.")
        return None
    record = Course.get_by_id(pk)
    if not record:
        print_error(f"No course found with ID {pk}.")
    return record


def add_course() -> None:
    print_header("Add New Course")
    try:
        name    = safe_input("  Course name : ", lambda v: validate_non_empty(v, "Course name"))
        code    = safe_input("  Course code : ", lambda v: validate_non_empty(v, "Course code"))
        credits = safe_input("  Credits     : ", lambda v: validate_integer(v, "Credits", 1))
        tid_str = safe_input("  Teacher ID  (Enter to skip): ",
                             lambda v: validate_integer(v, "Teacher ID", 1),
                             allow_blank=True)
        teacher_id = int(tid_str) if tid_str else None

        course = Course(name, code, credits, teacher_id)
        course.save()
        print_success(f"Course '{name}' added (ID={course.course_id}).")
    except KeyboardInterrupt:
        print("\n  Cancelled.")


def view_all_courses() -> None:
    print_header("All Courses")
    rows = Course.get_courses_with_teacher()
    print_table(rows, title="Courses with Teacher")


def update_course() -> None:
    print_header("Update Course")
    cid = input("  Enter course ID to update: ").strip()
    record = _get_course_or_error(cid)
    if not record:
        return
    try:
        name    = safe_input("  New course name  (Enter to keep): ",
                             lambda v: validate_non_empty(v, "Course name"),
                             allow_blank=True) or record["course_name"]
        code    = safe_input("  New course code  (Enter to keep): ",
                             lambda v: validate_non_empty(v, "Course code"),
                             allow_blank=True) or record["course_code"]
        cred_s  = safe_input("  New credits      (Enter to keep): ",
                             lambda v: validate_integer(v, "Credits", 1),
                             allow_blank=True)
        credits = int(cred_s) if cred_s else record["credits"]
        tid_s   = safe_input("  New teacher ID   (Enter to keep): ",
                             lambda v: validate_integer(v, "Teacher ID", 1),
                             allow_blank=True)
        tid     = int(tid_s) if tid_s else record["teacher_id"]

        course = Course(name, code, credits, tid, course_id=record["course_id"])
        if course.update():
            print_success("Course updated.")
        else:
            print_error("Update failed.")
    except KeyboardInterrupt:
        print("\n  Cancelled.")


def delete_course() -> None:
    print_header("Delete Course")
    cid = input("  Enter course ID to delete: ").strip()
    record = _get_course_or_error(cid)
    if not record:
        return
    confirm = input(f"  Delete '{record['course_name']}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Cancelled.")
        return
    if Course.delete_by_id(record["course_id"]):
        print_success("Course deleted.")
    else:
        print_error("Deletion failed.")


def search_courses() -> None:
    print_header("Search Courses")
    print("  Search by: 1) Course name  2) Course code")
    field_map = {"1": "course_name", "2": "course_code"}
    choice = input("  Choice: ").strip()
    field = field_map.get(choice)
    if not field:
        print_error("Invalid choice.")
        return
    term = input("  Search term: ").strip()
    results = Course.search(field, term)
    print_table(results, title=f"Search Results ({len(results)} found)")


def course_menu() -> None:
    options = {
        "1": ("Add course",       add_course),
        "2": ("View all courses", view_all_courses),
        "3": ("Update course",    update_course),
        "4": ("Delete course",    delete_course),
        "5": ("Search courses",   search_courses),
        "0": ("Back",             None),
    }

    while True:
        print_header("Course Management")
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
