from database.psql import get_psql_db_connection
import bcrypt
from enum import StrEnum
from logger_settings import setup_logger


logger = setup_logger("users")
logger.info("Запуск логов пользователей")

class UserRole(StrEnum):
    guest = "guest"
    user = "user"
    admin = "admin"

class DifferentPasswords(Exception):
    """Моё кастомное исключение."""
    def __init__(self, message="Введёные пароли не совпадают"):
        self.message = message
        logger.debug(message)
        super().__init__(self.message)

class EmailTaken(Exception):
    """Моё кастомное исключение."""
    def __init__(self, message="Пользователь с таким email уже существует"):
        self.message = message
        logger.debug(message)
        super().__init__(self.message)

def check_password(password: str, password_hash: bytes) -> bool:
    """Проверяет, соответствует ли пароль его хешу."""

    logger.debug("Запуск <check_password>")
    logger.info(f"Проверка пароля {password}")
    return bcrypt.checkpw(password.encode(), password_hash.tobytes())

def is_email_taken(email: str) -> bool:
    logger.debug("Запуск <is_email_taken>")
    logger.info(f"Проверка почты на занятость: {email}...")

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
        logger.info(f"Доступность почты {email}: {is_taken}")
        return is_taken
    except Exception as e:
        logger.error(f"Ошибка в is_email_taken({email}): {e}")
    finally:
        cur.close()
        conn.close()
    return False
    
def is_right_password(email: str, password: str) -> bool:
    logger.debug("Запуск <is_right_password>")
    logger.info(f"Проверка пароля {password} пользователя с почтой {email}")

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
        logger.error(f"Ошибка в функции is_right_password({email, password}): {e}")
        
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
    logger.debug("Запуск <check_user_login_data>")
    logger.info(
        f"Проверка данных для входа:\n"
        f"email: {email}"
        f"Пароль: {password}"
    )
    
    if not is_email_taken(email):
        return -1
    if is_right_password(email, password):
        return 1
    return 0

def get_user_id(email: str) -> int:
    logger.debug("Запуск <get_user_id>")
    logger.info(f"Получение user_id пользователя {email}...")

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
    return None

def get_user_data(user_id: int) -> dict:
    logger.debug("Запуск <get_user_data>")
    logger.info(f"Получение информации пользователя {user_id}...")

    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, username, email, created_at, role, password_hash "
            "FROM users WHERE id=%s",
            (user_id,)
        )
        user_data = cur.fetchone()
        logger.debug(user_data)
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
        logger.error(f"get_user_id({email}): {e}")
    finally:
        conn.close()
        cur.close()

def hash_password(password: str) -> bytes:
    """Хеширует пароль с использованием bcrypt."""
    logger.debug("Запуск <hash_password>")
    logger.info(f"Хеширование пароля {password}...")

    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode(), salt)
    password_hash_bytess = password_hash.decode()
    logger.info(f"Пароль хеширован")
    return password_hash_bytess

def add_user(username: str, email: str, password: str, role: UserRole = UserRole.user) -> int:
    """
    Добавляет пользователя, если это возможно.
    Возвращает id добавленного пользователя
    """
    logger.info(
        f"Попытка добавить пользователя:\n"
        f"email: {email}"
        f"username: {username}"
        f"passwords: {password}"
        f"role: {role}"
    )
    logger.debug("Запуск <add_user>")

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
        logger.error(
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
    logger.debug("Запуск <reg_user>")
    logger.info(
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
    logger.debug("Запуск <change_user_data_by_user_id>")
    logger.info(
        f"Смена данных пользователя {user_id} на\n"
        f"{new_user_data}"
    )

    def change_username(new_username: str) -> bool:
        logger.debug("Запуск <change_username>")
        logger.info(f"Смена имени на {new_username}")

        conn = get_psql_db_connection()
        cur = conn.cursor()
        try:    
            cur.execute(
                "UPDATE users "
                "SET username = %s "
                "WHERE id = %s;",
                (new_username, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Ошибка при смене имени: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        return False

    def change_email(new_email: str) -> bool:
        logger.debug("Запуск <change_email>")
        logger.info(f"Смена почты на {new_email}")

        conn = get_psql_db_connection()
        cur = conn.cursor()
        
        if is_email_taken(new_email):
            raise EmailTaken
        try:
            cur.execute(
                "UPDATE users "
                "SET email = %s "
                "WHERE id = %s;",
                (new_email, user_id)
            )
            conn.commit()
            logger.info("Почта изменена")
        except Exception as e:
            logger.error(f"Ошибка при изменении почты: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        return False
        
    def change_password(new_password: str) -> bool:
        logger.debug("Запуск <change_password>")
        logger.info(f"Смена имени на {new_password}")

        conn = get_psql_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "UPDATE users "
                "SET password_hash = %s "
                "WHERE id = %s;",
                (hash_password(new_password), user_id)
            )
            conn.commit()
            logger.info("Пароль изменён")
            return True
        except Exception as e:
            logger.error(f"Ошибка при смене пароля: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
            
        return False

    def compare_data(old_user_data: dict, new_user_data: dict):
        logger.debug("Запуск <compare_data>")
        logger.info(f"Смена данных с {old_user_data} на {new_user_data}")
        
        if old_user_data['username'] != new_user_data['username']:
            logger.info("Меняется имя")
            change_username(new_user_data['username'])
            
        if old_user_data['email'] != new_user_data['email']:
            logger.info("Меняется почта")
            change_email(new_user_data['email'])

        if not check_password(password_hash=old_user_data['password_hash'], password=new_user_data['password']):
            logger.info("Меняется пароль")
            change_password(new_user_data['password'])

    logger.info(f"Получение прежней информации пользователя {user_id}")
    old_user_data = get_user_data(user_id)
    logger.info(f"Информация получена")
    try:
        compare_data(old_user_data, new_user_data)
        return new_user_data
        
    except Exception as e:
        logger.error(f"Ошибка при изменении данных пользователя {user_id}: {e}")

    finally:
        return old_user_data
