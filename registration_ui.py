"""
registration_ui.py
CLI menu for Registration (enrolment) CRUD operations.
Author: Student
"""

from models.registration import Registration
from utils.display import print_header, print_success, print_error, print_table
from utils.validators import validate_integer, validate_grade, safe_input


def enrol_student() -> None:
    """Register a student to a course."""
    print_header("Enrol Student in Course")
    try:
        sid = safe_input("  Student ID : ", lambda v: validate_integer(v, "Student ID"))
        cid = safe_input("  Course ID  : ", lambda v: validate_integer(v, "Course ID"))
        grade = safe_input("  Grade (A/B/C/D/F or Enter to skip): ",
                           validate_grade, allow_blank=True)

        reg = Registration(int(sid), int(cid), grade if grade else None)
        reg.save()
        print_success(f"Student {sid} enrolled in course {cid}.")
    except Exception as err:
        print_error(f"Enrolment failed: {err}")


def view_all_registrations() -> None:
    print_header("All Registrations")
    rows = Registration.get_full_report()
    print_table(rows, title="Full Registration Report")


def update_registration() -> None:
    """Update the grade for a registration."""
    print_header("Update Registration Grade")
    rid = input("  Enter registration ID: ").strip()
    try:
        pk = int(rid)
    except ValueError:
        print_error("ID must be a number.")
        return
    record = Registration.get_by_id(pk)
    if not record:
        print_error(f"No registration with ID {pk}.")
        return

    grade = safe_input("  New grade (A/B/C/D/F or Enter to clear): ",
                       validate_grade, allow_blank=True)
    reg = Registration(
        record["student_id"], record["course_id"],
        grade if grade else None, registration_id=pk
    )
    if reg.update():
        print_success("Grade updated.")
    else:
        print_error("Update failed.")


def delete_registration() -> None:
    """Remove a student from a course."""
    print_header("Delete Registration")
    rid = input("  Enter registration ID to delete: ").strip()
    try:
        pk = int(rid)
    except ValueError:
        print_error("ID must be a number.")
        return
    record = Registration.get_by_id(pk)
    if not record:
        print_error(f"No registration with ID {pk}.")
        return
    confirm = input(
        f"  Remove student {record['student_id']} from course {record['course_id']}? (yes/no): "
    ).strip().lower()
    if confirm != "yes":
        print("  Cancelled.")
        return
    if Registration.delete_by_id(pk):
        print_success("Registration deleted.")
    else:
        print_error("Deletion failed.")


def registration_menu() -> None:
    options = {
        "1": ("Enrol student in course",       enrol_student),
        "2": ("View all registrations",         view_all_registrations),
        "3": ("Update registration grade",      update_registration),
        "4": ("Remove student from course",     delete_registration),
        "0": ("Back",                           None),
    }

    while True:
        print_header("Registration Management")
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
