# admin_panel.py
import sys
import os
from user_deletion import UserDeletion  # Import UserDeletion class
from tabulate import tabulate  # Ensure this library is installed: pip install tabulate

# Adjust sys.path to include parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import database connection
from db.db_connect import db_name

class AdminPanel:
    def __init__(self):
        self.show_menu()

    def show_menu(self):
        while True:
            print("\n--- Admin Panel ---")
            print("1. View Users")
            print("2. Manage User Deletions")
            print("3. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.manage_user_deletions()
            elif choice == "3":
                print("Exiting Admin Panel. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def view_users(self):
        print("\n--- User List ---")
        try:
            # Fetch users from the database
            user_collection = db_name['users']
            data = []
            sno = 1  # Initialize serial number
            for user in user_collection.find({}, {'username': 1, 'password': 1, '_id': 0}):  # Fetch relevant fields
                data.append([
                    sno,                              # Assign serial number
                    user.get('username', 'N/A'),      # Default to 'N/A' if username is missing
                    user.get('password', 'N/A')       # Default to 'N/A' if password is missing
                ])
                sno += 1  # Increment serial number

            # Print the data in table format
            headers = ["Sno", "Username", "Password"]
            print(tabulate(data, headers, tablefmt="grid"))
            print(f"\nTotal Number of Users: {len(data)}")
        except Exception as e:
            print(f"An error occurred while fetching users: {e}")

    def manage_user_deletions(self):
        print("\n--- Manage User Deletions ---")
        try:
            user_deletion = UserDeletion()  # Instantiate the UserDeletion class
            user_deletion.manage()  # Call the manage method
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Launch the Admin Panel
    AdminPanel()
