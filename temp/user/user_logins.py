import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.db_connect import db_name

print("Account login :-")
def user_login(username, password): 
    user_collection = db_name['users']
    user = user_collection.find_one({'username': username, 'password': password})
    if user:
        print("Login successful")
    else:
        print("Invalid username or password")

# Get user input first
usersname = input("Enter your username: ")
password = input("Enter your password: ")

# Now call the function after inputs are defined
user_login(usersname, password)
