import sys
import os
import uuid
from tabulate import tabulate
import msvcrt  # For Windows keyboard input
import time
from datetime import datetime, timedelta

# Adjust sys.path to include parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Import database connection and auth manager
from db.db_connect import db_name
from auth.auth_manager import AuthManager

class UserDataManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def handle_special_key(self, key):
        """Handle special keys"""
        if key == b'\x1b':  # ESC
            return 'ESC'
        elif key == b'\x08':  # Backspace
            return 'BACKSPACE'
        elif key == b'\x7f':  # Delete
            return 'DELETE'
        elif key == b'\x03':  # Ctrl+C
            return 'CTRL+C'
        return None

    def get_input(self, prompt):
        """Get input with special key support"""
        print(prompt, end='', flush=True)
        value = ""
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                special_key = self.handle_special_key(key)
                
                if special_key == 'ESC':
                    print("\nOperation cancelled.")
                    return None
                elif special_key == 'BACKSPACE':
                    if value:
                        value = value[:-1]
                        print('\b \b', end='', flush=True)
                    continue
                elif special_key == 'CTRL+C':
                    raise KeyboardInterrupt
                elif key == b'\r':  # Enter key
                    break
                else:
                    # Handle regular character input
                    try:
                        char = key.decode()
                        value += char
                        print(char, end='', flush=True)
                        continue
                    except UnicodeDecodeError:
                        continue
            time.sleep(0.1)  # Small delay to prevent CPU overuse
        return value.strip()

    def view_data(self):
        try:
            user_data = db_name.users.find_one({"_id": self.user_id})
            if user_data and "data" in user_data:
                print("\n--- Your Data ---")
                data = []
                for i, record in enumerate(user_data["data"], 1):
                    data.append([i, record.get("record_id", "N/A"), record.get("info", "N/A")])
                
                headers = ["Sno", "Record ID", "Info"]
                print(tabulate(data, headers, tablefmt="grid"))
            else:
                print("No data found.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return True

    def add_data(self):
        try:
            new_info = self.get_input("Enter new data (Press ESC to cancel): ")
            if not new_info:
                return True
                
            db_name.users.update_one(
                {"_id": self.user_id},
                {"$push": {"data": {"record_id": str(uuid.uuid4()), "info": new_info}}}
            )
            print("\nData added successfully.")
            return False
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return True

    def delete_data(self):
        try:
            record_id = self.get_input("Enter the record ID to delete (Press ESC to cancel): ")
            if not record_id:
                return True
                
            result = db_name.users.update_one(
                {"_id": self.user_id},
                {"$pull": {"data": {"record_id": record_id}}}
            )
            
            if result.modified_count > 0:
                print("\nData deleted successfully.")
            else:
                print("\nNo data found with the given record ID.")
            return False
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return True

    def show_menu(self):
        while True:
            try:
                print("\n--- User Data Manager ---")
                print("1. View Data")
                print("2. Add Data")
                print("3. Delete Data")
                print("4. Logout")
                print("\nPress ESC at any time to return to menu")
                print("Press Ctrl+C to exit")

                choice = self.get_input("Enter your choice: ")
                if not choice:  # ESC was pressed
                    continue

                if choice == "1":
                    if self.view_data():
                        continue
                elif choice == "2":
                    if self.add_data():
                        continue
                elif choice == "3":
                    if self.delete_data():
                        continue
                elif choice == "4":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please select a valid option.")
            except KeyboardInterrupt:
                print("\n\nExiting Password Manager. Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Returning to menu...")

def main():
    auth_manager = AuthManager()
    
    while True:
        try:
            print("\n=== Welcome to Password Manager ===")
            print("1. Login/Register")
            print("2. Forgot Password")
            print("3. Exit")
            print("\nPress Ctrl+C at any time to exit safely")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                if auth_manager.show_menu():  # Returns True if login successful
                    user = auth_manager.get_current_user()
                    user_manager = UserDataManager(user["user_id"])
                    user_manager.show_menu()
            elif choice == "2":
                if auth_manager.forgot_password():
                    print("\nPassword reset successful! Please check your email.")
                else:
                    print("\nPassword reset failed. Please try again.")
            elif choice == "3":
                print("\nThank you for using Password Manager. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please select a valid option.")
        except KeyboardInterrupt:
            print("\n\nExiting Password Manager. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Returning to main menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting Password Manager. Goodbye!")
