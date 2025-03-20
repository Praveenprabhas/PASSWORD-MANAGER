from pymongo import MongoClient


client = MongoClient('localhost',27017)

db_name = client['password_manager']


appdb_collection = db_name['appdata']
webdb_collection = db_name['webdata']
logindb_collection = db_name['login']


# print(client.list_database_names())
# print(db_name['database'])