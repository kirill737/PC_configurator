import psycopg2

PSQL_DB_CONFIG = {
    'dbname': 'pc_configurator_db',
    'user': 'kirill',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

def get_psql_db_connection():
    return psycopg2.connect(**PSQL_DB_CONFIG)