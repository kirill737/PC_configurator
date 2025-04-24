from database.redis import redis_client
from controllers.db.user_controller import get_user_data
import uuid

from logger_settings import setup_logger


logger = setup_logger("sessions")

logger.info("Запуск логера сессий")


def create_session(user_id: int) -> int:
    logger.debug("Запуск <create_session>")
    logger.info(f"Создание сессии пользователя: '{user_id}'")

    session_id = str(uuid.uuid4())  # Генерация уникального идентификатора сессии
    session_key = f"user_session:{session_id}"
    
    redis_client.hset(session_key, mapping=get_user_data(user_id))
    redis_client.expire(session_key, 3600)  # Сессия истечёт через 1 час (3600 секунд)
    
    redis_client.set(f"user:{user_id}:session", session_id, ex=3600)
    
    logger.info(f"Сессии пользователя: '{session_id}' создана")
    return session_id


def get_session_data(session_id: str) -> dict:
    logger.debug("Запуск <get_session_data>")
    session_key = f"user_session:{session_id}"
    session_data = redis_client.hgetall(session_key)
    logger.debug(f"Session data for {session_id}: {session_data}")
    return session_data


def delete_session(session_id: int) -> None:
    logger.debug("Запуск <delete_session>")
    session_key = f"user_session:{session_id}"
    redis_client.delete(session_key)
    logger.info(f"Сессия '{session_id}' - окончена")


def delete_session_by_user_id(user_id: int) -> None:
    logger.debug("Запуск <delete_session_by_user_id>")
    session_id = redis_client.get(f"user:{user_id}:session")
    logger.info(f"Попытка удаления сессии: '{session_id}' пользователя: {user_id}")
    
    if session_id:
        redis_client.delete(f"user_session:{session_id}")
        redis_client.delete(f"user:{user_id}:session")
        logger.info(f"Сессия '{session_id}' - окончена")