from pymongo import MongoClient


client = MongoClient('localhost',27017)

db_name = client['password_manager']



