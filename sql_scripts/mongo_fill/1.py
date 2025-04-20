from datetime import datetime, timedelta
from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")

db = client['mongo_db']
posts_collection = db['posts']

posts_collection.delete_many({})

with open("posts.ndjson", "r", encoding="utf-8") as f:
    for i, l in enumerate(f):
        d = json.loads(l)
        d["created_at"] = datetime.now() - timedelta(days=i)
        d["author"] = "name2"
        posts_collection.insert_one(d)


for post in posts_collection.find():
    print(post)


print()

from datetime import datetime, timedelta

three_days_ago = datetime.now() - timedelta(days=3)
recent_posts = db.posts.find({ "created_at": { "$gte": three_days_ago } })

for post in recent_posts:
    print(post["title"], post["created_at"])
