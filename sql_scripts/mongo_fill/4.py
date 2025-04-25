from datetime import datetime, timedelta
from pymongo import MongoClient
import json
import random 
from copy import deepcopy
random.seed(42)


client = MongoClient("mongodb://localhost:27017/")

db = client['mongo_db']
posts_collection = db['posts']

posts_collection.delete_many({})

setups = []
with open("builds.json", "r", encoding="utf-8") as f:
    for setup in json.load(f):
        new_setup = {}
        for ct in setup:
            new_setup[ct["ct_rus"]] = ct["name"]
        setups.append(new_setup)

print(setups)


users = [1, 2, 3, 5, 6]
for i in range(2, 102):
    d = deepcopy(random.choice(setups))
    d["created_at"] = datetime.now() - timedelta(days=random.randint(0, i//2))
    d["author_id"] = random.choice(users)
    print(posts_collection.insert_one(d))