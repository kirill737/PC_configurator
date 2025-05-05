from database.psql import get_psql_db_connection

from logger_settings import setup_logger
from controllers.db.component_controller import prepareType, get_component_data, get_all_component_types
from controllers.db.build_component_controller import connect_build_and_component

class AddBuildError(Exception):
    def __init__(self, message="Ошибка при создании сборки"):
        self.message = message
        logger.debug(message)
        super().__init__(self.message)

class BuildConnectionsError(Exception):
    def __init__(self, message="Ошибка при связывании сборки и комплектующих"):
        self.message = message
        logger.debug(message)
        super().__init__(self.message)

logger = setup_logger("build")
logger.info("Запуск build_controller")

def delete_build(build_id: int) -> None:
    logger.debug("Запуск <delete_build>")
    conn = get_psql_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(f"DELETE FROM builds WHERE id={build_id}")
        conn.commit()
    except Exception as e:
        logger.info(f"Ошибка при удалении сборки: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        
def get_build_info(build_id) -> list:
    logger.debug("Запуск <get_build_info>")
    logger.info(f"Получение комплектующих сборки '{build_id}'")
    
    conn = get_psql_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            "SELECT bc.component_id, c.type "
            "FROM build_components as bc "
            "LEFT JOIN components as c ON c.id = bc.component_id "
            f"WHERE bc.build_id = {build_id} "
            "ORDER BY bc.id"
            )
        all_types = get_all_component_types()
        raw_components_list = cur.fetchall()
        # cur.execute("SELECT name FROM")
        all_presented_types = [row[1] for row in raw_components_list]
        
        component_dicts = []
        row_index = 0
        for ct in all_types:
            if ct['ct'] in all_presented_types:
                row = raw_components_list[row_index]
                component_dicts.append(
                    {
                        "id": row[0],
                        "type": row[1],
                        "ct_rus": prepareType(row[1]),
                        "name": get_component_data(row[0])['name'] 
                    }
                )
                row_index += 1
            else:
                component_dicts.append(
                    {
                        "id": None,
                        "type": ct['ct'],
                        "ct_rus": ct['ct_rus'],
                        "name": None 
                    }
                )


        logger.debug(f"Component id list: '{component_dicts}'")
        logger.info("Данные сборки получены")
        
        return component_dicts
    except Exception as e:
        logger.error(f"Ошибка при получении деталей сборки: {e}")
        
        return None
    finally:
        cur.close()
        conn.close()

def create_build(user_id: int, name: str, build_info: dict) -> int:
    """
    Добавляет пользователя, если это возможно.
    Возвращает id созданной сборки
    """
    logger.debug("Запуск <create_build>")
    logger.info(f"Попытка создать сборку '{name}' от user_id: {user_id}...")
    logger.debug(f"Комплектующие: {build_info}")
    
    def add_build(user_id: int, name: str) -> int:
        conn = get_psql_db_connection()
        cur = conn.cursor()
    
        logger.debug("Запуск <add_build>")
        logger.info(f"Попытка добавить сборку '{name}' от user_id: {user_id}...")
        
        try:
            cur.execute(
                "INSERT INTO builds (user_id, name) "
                "VALUES (%s, %s) RETURNING id", 
                (user_id, name)
            )
            build_id = cur.fetchone()[0] 
            conn.commit()
            logger.info("Сборка создана!")
            return build_id
        except Exception as e:
            logger.error(f"Ошибка при создании сборки {e}")
            conn.rollback()
            raise AddBuildError
        finally:
            cur.close()
            conn.close()
        
    def connect_all_components(build_id: int, all_components: dict):
        logger.debug("Запуск <connect_all_components>")
        logger.info(f"Соединяем сборку '{build_id}' с комплекующими")
        
        conn = get_psql_db_connection()
        cur = conn.cursor()
        try:
            for _, component_id in all_components.items():
                if not connect_build_and_component(build_id, component_id):
                    raise Exception(f"Сборка '{build_id}' не связана с '{component_id}'")
            logger.info(f"Комплектующие связаны")
            conn.commit()
        except Exception as e:
            logger.error(f"Ошибка при связывании комплектующих: {e}")
            conn.rollback()
            raise BuildConnectionsError
        finally:
            cur.close()
            conn.close()
            
    conn = get_psql_db_connection()
    cur = conn.cursor()
    try:
        build_id = add_build(user_id, name)
        connect_all_components(build_id, build_info)
        conn.commit()
        return build_id
    except AddBuildError as e:
        logger.error(f"Ошибка при добавлении сборки: {e}")
        return None
    except BuildConnectionsError as e:
        logger.error(f"Ошибка при соединении сборки и комплектующих")
        delete_build(build_id)
        return None
    except Exception as e:
        logger.error(f"Ошибка при добавлении сборки: {e}")
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()

def get_user_builds(user_id: int) -> list:
    logger.debug("Запуск <get_user_builds>")
    logger.info(f"Попытка получить сборки пользователя '{user_id}'...")
    
    conn = get_psql_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(f"SELECT id, name FROM builds WHERE user_id={user_id}")
        builds = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
        logger.info(
            f"Сборки пользователя '{user_id}' получены\n"
            f"'{builds}'"
        )
        return builds
    except Exception as e:
        logger.error(f"Ошибка при получение сборок: {e}")
    finally:        
        cur.close()
        conn.close()
    return []



# def fill_build():
#     """
#     Добавляет пользователя, если это возможно.
#     Возвращает id добавленного пользователя
#     """
#     logger.debug("Запуск <add_build>")
#     logger.info(f"Попытка создать сборку '{name}' от user_id: {user_id}...")
#     logger.debug(f"Комплектующие: {build_info}")

#     conn = get_psql_db_connection()
#     cur = conn.cursor()

#     try:
#         cur.execute(
#             "INSERT INTO builds (user_id, name) "
#             "VALUES (%s, %s) RETURNING id", 
#             (user_id, name)
#         )
#         build_id = cur.fetchone()[0] 
#         for ct, info in build_info.items():
#             component_id = add_component(ct, info['price'], info)
#             if not component_id: # Проверка,что деталь добавилась 
#                 raise Exception(f"Деталь '{info['name']}' не была добавлена")
#             if not connect_build_and_component(build_id, component_id):
#                 raise Exception(f"Связь между {build_id} и {component_id} не установлена")
                                    
#         conn.commit()
#         logger.info("Сборка создана!")
#         return user_id
#     except Exception as e:
#         conn.rollback()
#         logger.error(
#             f"Ошибка при создании сборки '{name}' от user_id: {user_id}:\n"
#             f"{e}"
#         )
#         return None
#     finally:
#         cur.close()
#         conn.close()
