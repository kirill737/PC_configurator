import random
import string
from datetime import datetime, timedelta
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['mongo_db']
posts_collection = db['posts']
comments_collection = db['comments']

# Очистим старые комментарии
comments_collection.delete_many({})

def generate_random_text(min_words=5, max_words=15):
    words = []
    for _ in range(random.randint(min_words, max_words)):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)
    return ' '.join(words)

# # Для каждого поста создаем случайные комментарии
# for post in posts_collection.find():
#     num_comments = random.randint(1, 5)
#     for _ in range(num_comments):
#         comment = {
#             "post_id": post["_id"],
#             "text": generate_random_text(),
#             "user": f"user{random.randint(0, 10000)}",
#             "created_at": datetime.now() - timedelta(minutes=random.randint(0, 10000))
#         }
#         comments_collection.insert_one(comment)

# print("Комментарии успешно сгенерированы и сохранены в MongoDB ✅")
