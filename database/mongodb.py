from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['mongo_db']
posts_collection = db['posts']
comments_collection = db['comments']

per_page = 5


