import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.db_connect import db_name 


user = db_name['users']
print("Create a account :-")
while True:
    usersname = input("username : ").strip()
    username = usersname 

    if len(username) == 0:
        print("\nusername is empty.\n")
    elif user.find_one({"username": usersname}):
        print("\nusername already exists.\n")
    else:
        password = input("password : ").strip()
        password = password 
        if password == "":
                print("\npassword is empty.\n")
        else:   
                while True :    
                    numbers = "0123456789"
                    capital_letters = "ABCDEF"
                    small_letters = "abcdef"
                    symbols = "-"
                    all_characters = numbers + capital_letters + small_letters + symbols
                    random_string = ''.join(random.choice(all_characters) for _ in range(6))
                    uuid=random_string
                    # print("Random String:", random_string)
                    if user.find_one({"_id": uuid}):
                        continue
                    else:             
                        user.insert_one({"_id": uuid,"username": usersname, "password": password})
                        print("\nAccount created successfully.\n")
                        break
                break
        



