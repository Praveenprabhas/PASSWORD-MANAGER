from db_connect import client, db_name

class Admin:

    def __init__(self):
        self.home()

    def home(self):
        print("Welcome to the Database Control Page")
        print("1. Show collections")
        print("2. Delete collections")
        print("3. Delete database")
        print("4. Exit")
        self.choose = input("Enter your choice: ")
        if self.choose == "1":
            self.show_collections()
        elif self.choose == "2":
            self.delete_coll()
        elif self.choose == "3":
            self.delete_db()
        elif self.choose == "4":
            print("Exiting the password manager...")
            exit()
        else:
            print("Invalid choice")
            self.home()

    def show_collections(self):
        print("List of all the collections:")
        collections = db_name.list_collection_names()
        for collection in collections:
            print(collection)
        self.home()

    def delete_coll(self):
        collection_name = input("Enter the collection name to delete: ")
        if collection_name in db_name.list_collection_names():
            db_name[collection_name].drop()
            print(f"Collection '{collection_name}' deleted successfully.")
        else:
            print("Collection not found.")
        self.home()

    def delete_db(self):
        confirm = input("Are you sure you want to delete the entire database? (yes/no): ")
        if confirm.lower() == 'yes':
            client.drop_database(db_name)
            print(f"Database '{db_name}' deleted successfully.")
        else:
            print("Operation cancelled.")
        self.home()

# Instantiate the Admin class
myadmin = Admin()
