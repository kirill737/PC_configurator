from database.redis import redis_client
from controllers.session_controller import get_user_data
import uuid

def create_session(user_id: int) -> int:
    session_id = str(uuid.uuid4())  # Генерация уникального идентификатора сессии
    session_key = f"user_session:{session_id}"
    
    redis_client.hset(session_key, mapping=get_user_data(user_id))
    redis_client.expire(session_key, 3600)  # Сессия истечёт через 1 час (3600 секунд)
    
    return session_id

def get_session(session_id: int) -> dict:
    session_key = f"user_session:{session_id}"
    return redis_client.hgetall(session_key)  # Получаем все данные о сессии

def delete_session(session_id: int) -> None:
    session_key = f"user_session:{session_id}"
    redis_client.delete(session_key)

