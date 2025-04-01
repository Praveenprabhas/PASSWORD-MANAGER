import sys
import os
from tabulate import tabulate  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db_connect import db_name

class UserDeletion:
    def view_users(self):
        user_collection = db_name['users']
        data = []
        sno = 1  
        for user in user_collection.find({}, {'username': 1, '_id': 0}): 
            data.append([
                sno,                            
                user.get('username', 'N/A')     
            ])
            sno += 1  
        
        headers = ["Sno", "Username"]
        print(tabulate(data, headers, tablefmt="grid"))
        print(f"\nTotal Number of Users: {len(data)}")

    def verify(self):
        user_collection = db_name['users']  
        print("\nEnter username below to delete that user :-")
        username = input("Enter the username: ").strip()
        if not username:
            print("Input cannot be empty. Please enter a valid username.")
            return

        user = user_collection.find_one({"username": username})
        if user is None:
            print(f"User '{username}' does not exist.")
        else:
            password = input("Enter the password: ").strip()
            if not password:
                print("Password is empty.")
                return
            
            valid_user = user_collection.find_one({"username": username, "password": password})
            if valid_user:
                user_collection.delete_one({"username": username})
                print(f"User '{username}' deleted successfully.")
            else:
                print("Incorrect password.")

    def manage(self):
        while True:
            print("\n--- User Deletion Menu ---")
            print("1. View Users")
            print("2. Delete User")
            print("3. Back to Admin Panel")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.verify()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def __init__(self):
        pass
