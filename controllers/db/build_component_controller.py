from database.psql import get_psql_db_connection

from logger_settings import setup_logger

from controllers.db.component_controller import ComponentType as CT

logger = setup_logger("build_components")
logger.info("Запуск build_component_controller")

def change_build_component(build_id: int, old_id: int, new_id: int):
    def compare_components_type(component_id_1: int, component_id_2: int) -> bool:
        logger.info(f"Сравнение типов деталей '{component_id_1}' и '{component_id_2}'")
        
        conn = get_psql_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT type FROM components "
                f"WHERE id IN ({component_id_1}, {component_id_2}) "
                "LIMIT 2"
            )
            ct_1 = cur.fetchone()[0]
            ct_2 = cur.fetchone()[0]
            if ct_1 == ct_2:
                return True
            return False
        except Exception as e:
            logger.error(f"Ошибка при сравнении типов деталей: {e}")
        finally:
            cur.close()
            conn.close()
        return False
    
    conn = get_psql_db_connection()
    cur = conn.cursor()

    try:
        if old_id == new_id:
            logger.info(f"Выбрана текущая деталь")
            return True
        elif old_id is None:
            connect_build_and_component(build_id, new_id)
        if not compare_components_type(old_id, new_id):
            raise Exception(f"Типы деталей с id {old_id} и {new_id} не совпадают")

        cur.execute(
            "UPDATE build_components "
            f"SET component_id = {new_id} "
            f"WHERE build_id = {build_id} and component_id = {old_id}" 
        )
        
        conn.commit()
        logger.info(f"Изменение сборки '{build_id}': Успешная смена комплектующей '{old_id}' на '{new_id}'")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(
            f"Ошибка при изменении сборки '{build_id}': комплектующей '{old_id}' на '{new_id}'.\n"
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
    
def get_component_id(build_id: int, ct: CT):
    logger.info(f"Попытка получить component_id в сборке '{build_id}' с типом {ct}")
    conn = get_psql_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT c.id AS component_id "
            "FROM build_components bc "
            "JOIN components c ON bc.component_id = c.id "
            f"WHERE bc.build_id = {build_id} AND c.type = '{ct}'"
        )
        component_id = cur.fetchone()[0]
        logger.info(f"Получен component_id в сборке '{build_id}' с типом {ct}")
        return component_id
    except Exception as e:
        conn.rollback()
        logger.error(
            f"Ошибка при получении component_id в сборке '{build_id}' с типом {ct}:\n"
            f"{e}"
        )
    finally:
        cur.close()
        conn.close()
    
    return None