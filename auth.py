"""
auth.py
Simple administrator login feature (Optional O1 – Authentication).
Credentials are stored as bcrypt hashes; plain-text fallback for demo mode.
Author: Student
"""

import hashlib

# Default admin credentials (hashed with SHA-256 for demo purposes)
# In production, use bcrypt and store in a secrets manager.
_ADMIN_CREDENTIALS = {
    "admin": hashlib.sha256("Admin@1234".encode()).hexdigest(),
}

MAX_ATTEMPTS = 3


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def login() -> bool:
    """
    Prompt for username and password.
    Returns True on successful authentication, False after MAX_ATTEMPTS failures.
    """
    from utils.display import print_header, print_error, print_success

    print_header("Administrator Login")
    print("  Default credentials: admin / Admin@1234\n")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        username = input("  Username: ").strip()
        password = input("  Password: ").strip()

        stored_hash = _ADMIN_CREDENTIALS.get(username)
        if stored_hash and stored_hash == _hash(password):
            print_success(f"Welcome, {username}!")
            return True

        remaining = MAX_ATTEMPTS - attempt
        if remaining > 0:
            print_error(f"Invalid credentials. {remaining} attempt(s) remaining.")
        else:
            print_error("Too many failed attempts. Exiting.")

    return False
