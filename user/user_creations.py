import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.db_connect import db_name  # Now it should work


user = db_name['users']
print("Create a account :-")
while True:
    usersname = input("username : ")
    username = usersname  # assign the input to the variable

    if len(username) == 0:  # corrected the condition
        print("\nusername is empty.\n")
    elif user.find_one({"username": usersname}):  # corrected the find_one method
        print("\nusername already exists.\n")
    else:
        password = input("password : ")
        password = password  # assign the input to the variable
        if password == "":
                print("\npassword is empty.\n")
        else:       
                
                user.insert_one({"username": usersname, "password": password})
                print("\nAccount created successfully.\n")
                break
        



