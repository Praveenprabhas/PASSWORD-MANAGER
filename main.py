import sys
import os


class UserDataManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def view_data(self):
        user_data = db_name.users.find_one({"user_id": self.user_id})
        if user_data and "data" in user_data:
            print("Your Data:")
            for record in user_data["data"]:
                print(record)
        else:
            print("No data found.")

    def add_data(self):
        new_info = input("Enter new data: ")
        db_name.users.update_one(
            {"user_id": self.user_id},
            {"$push": {"data": {"record_id": str(uuid.uuid4()), "info": new_info}}}
        )
        print("Data added successfully.")

    def delete_data(self):
        record_id = input("Enter the record ID to delete: ")
        db_name.users.update_one(
            {"user_id": self.user_id},
            {"$pull": {"data": {"record_id": record_id}}}
        )
        print("Data deleted successfully.")

# Example Usage
logged_in_user_id = "user123"  # This would be retrieved during login
user_manager = UserDataManager(logged_in_user_id)
user_manager.view_data()
user_manager.add_data()
user_manager.delete_data()
