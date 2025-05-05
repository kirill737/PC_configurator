from datetime import datetime, timedelta
from pymongo import MongoClient
import string
import json
import random 
from copy import deepcopy
random.seed(42)


client = MongoClient("mongodb://localhost:27017/")

db = client['mongo_db']
posts_collection = db['posts']

posts_collection.delete_many({})


def generate_random_text(min_words=5, max_words=15):
    words = []
    for _ in range(random.randint(min_words, max_words)):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)
    return ' '.join(words)


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
    title, content = generate_random_text(1, 3 + 1), generate_random_text(0, 40)
    if title:
        d["title"] = title
    if content:
        d["content"] = content
    d["created_at"] = datetime.now() - timedelta(days=random.randint(0, i//2))
    d["author_id"] = random.choice(users)
    print(posts_collection.insert_one(d))