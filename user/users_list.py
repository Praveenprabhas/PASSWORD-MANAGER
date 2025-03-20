import sys
import os
from tabulate import tabulate  # Ensure you install this library: pip install tabulate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db_connect import db_name

# Assuming db_name['users'] is a MongoDB collection
user_collection = db_name['users']

# Fetch the data
data = []
for user in user_collection.find({}, {'sno': 1, 'username': 1, 'password': 1, '_id': 0}):  # Get specific fields
    data.append([user['sno'], user['username'], user['password']])

# Print in table format
headers = ["Sno", "Username", "Password"]
print(tabulate(data, headers, tablefmt="grid"))
