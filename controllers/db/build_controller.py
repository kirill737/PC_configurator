from database.psql import get_psql_db_connection

# from enum import StrEnum
from logger_settings import setup_logger
from controllers.db.component_controller import add_component, ComponentType

logger = setup_logger("build")
logger.info("Запуск build_controller")

def add_build(user_id: int, name: str, build_info: dict) -> int:
    """
    Добавляет пользователя, если это возможно.
    Возвращает id добавленного пользователя
    """
    logger.info("Запуск <add_build>")
    logger.info(
        f"Попытка создать сборку:\n"
        f"user_id: {user_id}"
        f"Комплектующие: {dict}"
    )

    conn = get_psql_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO builds (user_id, name) "
            "VALUES (%s, %s) RETURNING id", 
            (user_id, name)
        )
        for ct, info in build_info.items():
            add_component(ct, info['price'], info)
        user_id = cur.fetchone()[0]                     
        conn.commit()
        return user_id
    except Exception as e:
        conn.rollback()
        logger.error(
            f"Ошибка при создании сборки:\n"
            f"user_id: {user_id}"
            f"Комплектующие: {dict}"
        )
        return None
    finally:
        cur.close()
        conn.close()

# def reg_user(username: str, email: str, password_1: str, password_2: str) -> int:
#     logger.info("Запуск <reg_user>")
#     logger.info(
#         f"Попытка регистрации:\n"
#         f"email: {email}"
#         f"username: {username}"
#         f"passwords: {password_1} - {password_2}"
#     )
#     if password_1 != password_2:
#         raise DifferentPasswords
#     else:
#         password = password_2

#     if is_email_taken(email):
#         raise EmailTaken
    
#     return add_user(username, email, password)