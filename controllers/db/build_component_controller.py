from database.psql import get_psql_db_connection

# from enum import StrEnum
from logger_settings import setup_logger

logger = setup_logger("build_components")
logger.info("Запуск build_component_controller")



def connect_build_and_component(build_id: int, component_id: int, amount: int = 1):
    conn = get_psql_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO build_components (build_id, component_id, amount) "
            "VALUES (%s, %s, %s) RETURNING id", 
            (build_id, component_id, amount)
        )
                   
        conn.commit()
        logger.info(f"Связь между сборкой: '{build_id}' и комплектующей: '{component_id}' - установлена!")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(
            f"Ошиюка при связыванние сборки: '{build_id}' и комплектующей: '{component_id}' - не установлена"
            f"{e}"
        )
    finally:
        cur.close()
        conn.close()
    return False
    