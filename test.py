import psycopg2

PSQL_DB_CONFIG = {
    'dbname': 'pc_config_db',
    'user': 'kirill',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

def get_psqsl_db_connection():
    return psycopg2.connect(**PSQL_DB_CONFIG)

conn = get_psqsl_db_connection()
cur = conn.cursor()
name = ""
email = "kirill737apple@yandex.ru"

cur.execute(f"SELECT * FROM users WHERE email='{email}'") 
print(cur.fetchone()[0])
# user_id = cur.fetchone()[0]                         
conn.commit()
cur.close()
conn.close()