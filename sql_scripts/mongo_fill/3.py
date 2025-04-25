import random
import string
from datetime import datetime, timedelta
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['mongo_db']
posts_collection = db['posts']
comments_collection = db['comments']


for post in posts_collection.find():
    print(post)


print()


for comment in comments_collection.find():
    print(comment)