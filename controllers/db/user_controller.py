from database.psql import get_psqsl_db_connection
from controllers.password_controller import check_password, hash_password

conn = get_psqsl_db_connection()
cur = conn.cursor()
def is_unique_user(email: str):
    cur.execute("SELECT * FROM users WHERE email = '%s',",
                (email))
    return cur.fetchone()
def add_user(name: str, email: str, raw_password: str):
    conn = get_psqsl_db_connection()
    cur = conn.cursor()
    def is_unique_user(email: str):
        cur.execute("SELECT * FROM users WHERE email = '%s',",
                    (email))
        return cur.fetchone()
    
    password_hash = hash_password(raw_password)
    try:
        cur.execute("INSERT INTO users (name, email, password_hash)"
                    "VALUES (%s, %s, %s) RETURNING id",
                    (name, email, password_hash))
        component_id = cur.fetchone()[0]                         
        
        conn.commit()
        return component_id
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при добавлении пользователя: {e}")
        return None
    finally:
        cur.close()
        conn.close()

print(is_unique_user("ivan@example.com"))
