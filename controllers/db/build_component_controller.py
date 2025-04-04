from database.psql import get_psql_db_connection

# from enum import StrEnum
from logger_settings import setup_logger

logger = setup_logger("build_components")
logger.info("Запуск build_component_controller")


def update_component(build_id: int, old_id: int, new_id: int):
    conn = get_psql_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "UPDATE build_components "
            f"SET component_id = {new_id} "
            f"WHERE build_id = {build_id} and component_oid = {old_id}" 
        )
        
        conn.commit()
        logger.info(f"Изменение сборки '{build_id}': Успешная смена комплектующей '{old_id}' на '{new_id}'")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(
            f"Ошиюка при изменении сборки '{build_id}': омплектующей '{old_id}' на '{new_id}'.\n"
            f"{e}"
        )
    finally:
        cur.close()
        conn.close()
    return 
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
    