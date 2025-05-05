import random
import string
from datetime import datetime, timedelta
from pymongo import MongoClient
import random

client = MongoClient("mongodb://localhost:27017/")
db = client['mongo_db']
posts_collection = db['posts']
comments_collection = db['comments']

# Очистим старые комментарии
comments_collection.delete_many({})


words = [
    "good", "bad", "not bad", "nice", "noooo", "yeaaaaa", "leave", "super", "amazing", 
    "so so", "WHAT", "...................", ":)", ":(", "))))))))", "!!))!)!)!", "((((", 
    "maaaaaaaaaaaaaaannn", "ddaaaaaaaaaaaaaaaaaaaaamn", "10/10", "0/10", "Мусорка", 
    "тарахтелка", "динозавр", "позор", "в кс 20fps", "комп дотера", "ну ты и задрот",
    "у меня потекли слюни", "мощный комп", "за скок брал видюху?", "уже пробовал майнить на видюхе?",
    "мажор", "удали пост и не позорься", "красава чел круто флексишь", "НУ ПОЧЕМУ ОН А НЕ Я",
    "ну чисто тиктоки можно полистать на таком сетапчике", "давно брал?", "главное моник не разбить когда в кс играешь",
    "сетап дотера пон", "красотааааааааааааааа", "да ты прям эстет", "не хватает только моника 8K во всю стену",
    "приставки лучше", "компы это в целом отстой, не знаю чем вы тут меритесь", "ддададад комп за 300 тыщ и моник 60fps КРАСАВА",
    "чел...", "подарите мне такой же на день рождения пожалуйста", "питоновские скрипты потянет?"
]


users = ["name2", "name3", "admin", "name111", "kir"]
# Для каждого поста создаем случайные комментарии
for post in posts_collection.find():
    num_comments = random.randint(1, 5)
    for _ in range(num_comments):
        comment = {
            "post_id": post["_id"],
            "text": random.choice(words),
            "user": random.choice(users),
            "created_at": datetime.now() - timedelta(minutes=random.randint(0, 10000))
        }
        comments_collection.insert_one(comment)

print("Комментарии успешно сгенерированы и сохранены в MongoDB ✅")
