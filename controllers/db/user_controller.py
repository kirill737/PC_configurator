from database.psql import get_psql_db_connection
import bcrypt
import psycopg2

def hash_password(password: str) -> bytes:
    """Хеширует пароль с использованием bcrypt."""
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode(), salt)
    return password_hash.decode()

def check_password(password: str, password_hash: bytes) -> bool:
    """Проверяет, соответствует ли пароль его хешу."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())

def is_user_exist(email: str) -> bool:
    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        return user != None
    except Exception as e:
        print(f"Ошибка is_user_exist({email}): {e}")
    finally:
        cur.close()
        conn.close()
    return False
    

def is_right_password(email: str, password: str):
    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT password_hash FROM users WHERE email='{email}'") 
        password_hash = cur.fetchone()[0].tobytes()
        isCorrectPassword = bcrypt.checkpw(password.encode(), password_hash)
        return isCorrectPassword
    except Exception as e:
        print(f"Ошибка is_right_password({email, password}): {e}")
    finally:
        cur.close()
        conn.close()
    return False
    

def check_user_data(email: str, password: str) -> int:
    """
    -1 - пользователя с заданной почтой нет
    0 - неверный пароль
    1 - верный пароль
    """
    if not is_user_exist(email):
        return -1
    if is_right_password(email, password):
        return 1
    return 0

def get_user_id(email: str):
    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT id FROM users WHERE email='{email}'")
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
        cur.execute(f"SELECT id, name, email, created_at, role FROM users WHERE id='{user_id}'")
        user_data = cur.fetchone()
        # user_id = user_data[0]
        username = user_data[1]
        email = user_data[2]
        created_at = user_data[3]
        role = user_data[4]
        result = {
            'user_id': user_id,
            'uesrname': username,
            'email': email,
            'created_at': created_at,
            'role': role
        }
        # print(f"Logged user_id: {user_id} {type(user_id)}")
        return result
    except Exception as e:
        print(f"Ошибка get_user_id({email}): {e}")
    finally:
        conn.close()
        cur.close()
def add_user(name: str, email: str, password: str, role: str = "user"):
    """
    Добавляет пользователя, если это возможно.
    Возвращает id добавленного пользователя
    """
    if is_user_exist(email):
        print("Пользователь с таким email уже существует")
        return None

    password_hash = hash_password(password)
    conn = get_psql_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s) RETURNING id", 
                    (name, email, password_hash, role))
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




    

