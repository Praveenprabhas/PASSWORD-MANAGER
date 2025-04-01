import sys
import os
import bcrypt
import re
from datetime import datetime, timezone

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Connect to MongoDB
from db.db_connect import db_name
user_collection = db_name['users']

def hash_password(password):
    """Hashes the password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def is_valid_email(email):
    """Validates email format"""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email)

print("Create an account:")
while True:
    username = input("Username: ").strip().lower()
    
    if not username:
        print("\nUsername cannot be empty.\n")
        continue

    # Check if username already exists
    if user_collection.find_one({"username": username}):
        print("\nUsername already exists. Try another.\n")
        continue

    email = input("Email: ").strip().lower()

    if not email:
        print("\nEmail cannot be empty.\n")
        continue

    if not is_valid_email(email):
        print("\nInvalid email format.\n")
        continue

    # Check if email already exists
    if user_collection.find_one({"email": email}):
        print("\nEmail is already registered.\n")
        continue

    password = input("Password: ").strip()

    if not password:
        print("\nPassword cannot be empty.\n")
        continue

    hashed_password = hash_password(password)

    # Insert new user into the database
    user_data = {
        "username": username,
        "email": email,
        "password_hash": hashed_password,
        "created_at": datetime.now(timezone.utc)  # Timezone-aware datetime
    }

    user_collection.insert_one(user_data)

    print("\nAccount created successfully!\n")
    break  # Exit loop after successful registration
