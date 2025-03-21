import sys
import os
from tabulate import tabulate  # Ensure you install this library: pip install tabulate

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
        print("Enter username below to delete that user :-")
        username = input("Enter the username: ").strip()
        if not username:
            print("Input cannot be empty. Please enter a valid username.")
        else:
 user = user_collection.find_one({"username": username})
    if user is None:
        print(f"User '{username}' does not exist.")
    else:
        print(f"User '{username}' already exists.")

    def __init__(self):
        self.view_users()
        self.verify()
        

delete = UserDeletion()
