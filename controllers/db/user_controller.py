from database.psql import get_psql_db_connection
import bcrypt
import psycopg2
from enum import StrEnum
import logging

logging.basicConfig(
    filename="logs/pc_config_users.log",  # Лог в файл
    level=logging.DEBUG,  # Логируем всё (DEBUG и выше)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат вывода
    datefmt="%Y-%m-%d %H:%M:%S"
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
    return bcrypt.checkpw(password.encode(), password_hash.encode())

def is_email_taken(email: str) -> bool:
    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, password_hash"
            "FROM users WHERE email = %s;",
            (email,)
        )
        user = cur.fetchone()
        return user != None
    except Exception as e:
        print(f"Ошибка is_email_taken({email}): {e}")
    finally:
        cur.close()
        conn.close()
    return False
    
def is_right_password(email: str, password: str):
    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT password_hash"
            "FROM users WHERE email=%s;",
            (email,)
        ) 
        password_hash = cur.fetchone()[0].tobytes()
        isCorrectPassword = bcrypt.checkpw(password.encode(), password_hash)
        return isCorrectPassword
    except Exception as e:
        print(f"Ошибка is_right_password({email, password}): {e}")
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
    if not is_email_taken(email):
        return -1
    if is_right_password(email, password):
        return 1
    return 0

def get_user_id(email: str):
    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id FROM users"
            "WHERE email=%s",
            (email,)
        )
        # print(f"Email: {email}")
        user_id = cur.fetchone()[0]
        # print(f"Logged user_id: {user_id} {type(user_id)}")
        return user_id
    except Exception as e:
        print(f"Ошибка get_user_id({email}): {e}")
    finally:
        conn.close()
        cur.close()

def get_user_data(user_id: int) -> dict:
    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, username, email, created_at, role"
            "FROM users WHERE id=%s",
            (user_id,)
        )
        user_data = cur.fetchone()
        # user_id = user_data[0]
        username = user_data[1]
        email = user_data[2]
        # created_at = user_data[3]
        role = user_data[4]
        result = {
            'user_id': user_id,
            'username': username,
            'email': email,
            # 'created_at': created_at,
            'role': role
        }
        # print(f"Logged user_id: {user_id} {type(user_id)}")
        return result
    except Exception as e:
        print(f"Ошибка get_user_id({email}): {e}")
    finally:
        conn.close()
        cur.close()
        
def add_user(username: str, email: str, password: str, role: UserRole = UserRole.user) -> int:
    logging.info(
        f"Попытка добавить пользователя:\n"
        f"email: {email}"
        f"username: {username}"
        f"passwords: {password}"
        f"role: {role}"
    )
    """
    Добавляет пользователя, если это возможно.
    Возвращает id добавленного пользователя
    """
    def hash_password(password: str) -> bytes:
        """Хеширует пароль с использованием bcrypt."""
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)
        return password_hash.decode()

    if is_email_taken(email):
        print("Пользователь с таким email уже существует")
        raise EmailTaken
        return None

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
        print(f"Ошибка при добавлении пользователя: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def reg_user(username: str, email: str, password_1: str, password_2: str) -> int:
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

def change_user_data_by_user_id(user_id: int):
    conn = get_psql_db_connection()
    cur = conn.cursor()
    def change_username(new_username: str, ) -> bool:
        try: 
            cur.execute(
                "UPDATE users"
                "SET username = %s"
                "WHERE id = %s;",
                (new_username, user_id)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при изменении имени: {e}")
            return None
        # finally:
        #     cur.close()
        #     conn.close()
    def change_email(new_email: str) -> bool:
        try: 
            cur.execute(
                "UPDATE users"
                "SET email = %s"
                "WHERE id = %s;",
                (new_email, user_id)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при изменении имени: {e}")
            return None
        # finally:
        #     cur.close()
        #     conn.close()

        

    if is_email_taken():
        raise EmailTaken

    # cur.execute(
    #     "UPDATE users"
    #     "SET ")
    







    

