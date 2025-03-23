from database.psql import get_psql_db_connection
import bcrypt
import psycopg2
from enum import StrEnum
import logging

logging.basicConfig(
    filename="logs/pc_config_users.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)

class UserRole(StrEnum):
    guest = "guest"
    user = "user"
    admin = "admin"

class DifferentPasswords(Exception):
    """Моё кастомное исключение."""
    def __init__(self, message="Введёные пароли не совпадают"):
        self.message = message
        logging.debug(message)
        super().__init__(self.message)

class EmailTaken(Exception):
    """Моё кастомное исключение."""
    def __init__(self, message="Пользователь с таким email уже существует"):
        self.message = message
        logging.debug(message)
        super().__init__(self.message)

def check_password(password: str, password_hash: bytes) -> bool:
    """Проверяет, соответствует ли пароль его хешу."""

    logging.info("Запуск <check_password>")
    logging.info(f"check_password -> Проверка пароля {password}")
    return bcrypt.checkpw(password.encode(), password_hash.encode())

def is_email_taken(email: str) -> bool:
    logging.info("Запуск <is_email_taken>")
    logging.info(f"Проверка почты на занятость: {email}...")

    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, password_hash "
            "FROM users WHERE email = %s;",
            (email,)
        )
        user = cur.fetchone()
        is_taken = user is not None
        logging.info(f"Доступность почты {email}: {is_taken}")
        return is_taken
    except Exception as e:
        logging.error(f"Ошибка в is_email_taken({email}): {e}")
    finally:
        cur.close()
        conn.close()
    return False
    
def is_right_password(email: str, password: str):
    logging.info("Запуск <is_right_password>")
    logging.info(f"Проверка пароля {password} пользователя с почтой {email}")

    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT password_hash "
            "FROM users WHERE email=%s;",
            (email,)
        ) 
        password_hash = cur.fetchone()[0].tobytes()
        isCorrectPassword = bcrypt.checkpw(password.encode(), password_hash)
        return isCorrectPassword
    except Exception as e:
        logging.error(f"Ошибка в функции is_right_password({email, password}): {e}")
        
    finally:
        cur.close()
        conn.close()
    return False
    

def check_user_login_data(email: str, password: str) -> int:
    """
    -1 - пользователя с заданной почтой нет
    0 - неверный пароль
    1 - верный пароль
    """
    logging.info("Запуск <check_user_login_data>")
    logging.info(
        f"Проверка данных для входа:\n"
        f"email: {email}"
        f"Пароль: {password}"
    )
    
    if not is_email_taken(email):
        return -1
    if is_right_password(email, password):
        return 1
    return 0

def get_user_id(email: str):
    logging.info("Запуск <get_user_id>")
    logging.info(f"Получение user_id пользователя {email}...")

    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id FROM users "
            "WHERE email=%s",
            (email,)
        )
        user_id = cur.fetchone()[0]
        return user_id
    except Exception as e:
        print(f"Ошибка get_user_id({email}): {e}")
    finally:
        conn.close()
        cur.close()

def get_user_data(user_id: int) -> dict:
    logging.info("Запуск <get_user_data>")
    logging.info(f"Получение информации пользователя {user_id}...")

    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, username, email, created_at, role, password_hash "
            "FROM users WHERE id=%s",
            (user_id,)
        )
        user_data = cur.fetchone()
        logging.debug(user_data)
        # user_id = user_data[0]
        username = user_data[1]
        email = user_data[2]
        # created_at = user_data[3]
        role = user_data[4]
        password_hash = user_data[5]
        result = {
            'user_id': user_id,
            'username': username,
            'email': email,
            # 'created_at': created_at,
            'role': role,
            'password_hash': password_hash
        }
        return result
    except Exception as e:
        logging.error(f"get_user_id({email}): {e}")
    finally:
        conn.close()
        cur.close()

def hash_password(password: str) -> bytes:
    """Хеширует пароль с использованием bcrypt."""
    logging.info("Запуск <hash_password>")
    logging.info(f"Хеширование пароля {password}...")

    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode(), salt)
    return password_hash.decode()

def add_user(username: str, email: str, password: str, role: UserRole = UserRole.user) -> int:
    """
    Добавляет пользователя, если это возможно.
    Возвращает id добавленного пользователя
    """
    logging.info(
        f"Попытка добавить пользователя:\n"
        f"email: {email}"
        f"username: {username}"
        f"passwords: {password}"
        f"role: {role}"
    )
    logging.info("Запуск <add_user>")

    if is_email_taken(email):
        raise EmailTaken

    password_hash = hash_password(password)
    conn = get_psql_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, email, password_hash, role)"
            "VALUES (%s, %s, %s, %s) RETURNING id", 
            (username, email, password_hash, role)
        )
        user_id = cur.fetchone()[0]                     
        conn.commit()
        return user_id
    except Exception as e:
        conn.rollback()
        logging.error(
            f"Ошибка при добавлении пользователя: {e}\n"
            f"email: {email}\n"
            f"username: {username}\n"
            f"passwords: {password}\n"
            f"role: {role}"
        )
        return None
    finally:
        cur.close()
        conn.close()

def reg_user(username: str, email: str, password_1: str, password_2: str) -> int:
    logging.info("Запуск <reg_user>")
    logging.info(
        f"Попытка регистрации:\n"
        f"email: {email}"
        f"username: {username}"
        f"passwords: {password_1} - {password_2}"
    )
    if password_1 != password_2:
        raise DifferentPasswords
    else:
        password = password_2

    if is_email_taken(email):
        raise EmailTaken
    
    return add_user(username, email, password)

def change_user_data_by_user_id(user_id: int, new_user_data: dict) -> dict:
    logging.info("Запуск <change_user_data_by_user_id>")
    logging.info(
        f"Смена данных пользователя {user_id} на\n"
        f"{new_user_data}"
    )

    conn = get_psql_db_connection()
    cur = conn.cursor()
    
    def change_username(new_username: str):
        logging.info("Запуск <change_username>")
        logging.info(f"Смена имени на {new_username}")

        cur.execute(
            "UPDATE users "
            "SET username = %s "
            "WHERE id = %s;",
            (new_username, user_id)
        )

    def change_email(new_email: str):
        logging.info("Запуск <change_email>")
        logging.info(f"Смена имени на {new_email}")

        if is_email_taken():
            raise EmailTaken
        cur.execute(
            "UPDATE users "
            "SET email = %s "
            "WHERE id = %s;",
            (new_email, user_id)
        )
    
    def change_password(new_password: str):
        logging.info("Запуск <change_password>")
        logging.info(f"Смена имени на {new_password}")

        cur.execute(
            "UPDATE users "
            "SET password_hash = %s "
            "WHERE id = %s;",
            (hash_password(new_password), user_id)
        )

    def compare_data(old_user_data: dict, new_user_data: dict):
        logging.info("Запуск <compare_data>")
        logging.info(f"Смена данных с {old_user_data} на {old_user_data}")
        
        if old_user_data['username'] != new_user_data['username']:
            logging.info("Меняется имя")
            change_username(new_user_data['username'])
            
        if old_user_data['email'] != new_user_data['email']:
            logging.info("Меняется почта")
            change_email(new_user_data['email'])

        if old_user_data['password_hash'] != new_user_data['password_hash']:
            logging.info("Меняется пароль")
            change_password(new_user_data['password_hash'])

    old_user_data = get_user_data(user_id)

    try:
        compare_data(old_user_data, new_user_data)
        conn.commit()
        return new_user_data
        
    except Exception as e:
        conn.rollback()
        logging.error(f"Ошибка при изменении данных пользователя {user_id}: {e}")

    finally:
        cur.close()
        conn.close()
        return old_user_data
