import sys
import os
from tabulate import tabulate  # Ensure you install this library: pip install tabulate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db_connect import db_name

# Assuming db_name['users'] is a MongoDB collection
user_collection = db_name['users']

# Fetch the data
data = []
sno = 1  # Initialize serial number
for user in user_collection.find({}, {'username': 1, 'password': 1, '_id': 0}):  # Fetch only relevant fields
    data.append([
        sno,                             # Assign serial number
        user.get('username', 'N/A'),     # Default to 'N/A' if 'username' is missing
        user.get('password', 'N/A')      # Default to 'N/A' if 'password' is missing
    ])
    sno += 1  # Increment the serial number

# Print in table format
headers = ["Sno", "Username", "Password"]
print(tabulate(data, headers, tablefmt="grid"))

# Print total number of users
print(f"\nTotal Number of Users: {len(data)}")
