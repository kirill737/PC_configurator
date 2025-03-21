from database.redis import redis_client
from controllers.db.user_controller import get_user_data
import uuid
import logging

logging.basicConfig(
    filename="logs/pc_config_sesions.log",  # Лог в файл
    level=logging.INFO,  # Логируем всё (DEBUG и выше)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат вывода
    datefmt="%Y-%m-%d %H:%M:%S"
)

def create_session(user_id: int) -> int:
    logging.info(f"Создание сессии пользователя: {user_id}")

    session_id = str(uuid.uuid4())  # Генерация уникального идентификатора сессии
    session_key = f"user_session:{session_id}"
    
    redis_client.hset(session_key, mapping=get_user_data(user_id))
    redis_client.expire(session_key, 3600)  # Сессия истечёт через 1 час (3600 секунд)
    
    redis_client.set(f"user:{user_id}:session", session_id, ex=3600)
    
    return session_id

def get_session_data(session_id: int) -> dict:
    session_key = f"user_session:{session_id}"
    return redis_client.hgetall(session_key)  # Получаем все данные о сессии

def delete_session(session_id: int) -> None:
    session_key = f"user_session:{session_id}"
    redis_client.delete(session_key)
    logging.info(f"Сессия {session_id} - окончена")

def delete_session_by_user_id(user_id: int) -> None:
    session_id = redis_client.get(f"user:{user_id}:session")
    logging.info(f"Конец сессии {session_id} пользователя {user_id}")
    
    if session_id:
        redis_client.delete(f"user_session:{session_id}")  # Удаляем данные сессии
        redis_client.delete(f"user:{user_id}:session")  # Удаляем индекс
        logging.info(f"Сессия {session_id} - окончена")

