from controllers.db.components.case_controller import insert_case_query
from controllers.db.components.cpu_controller import insert_cpu_query
from controllers.db.components.gpu_controller import insert_gpu_query
from controllers.db.components.headphones_controller import insert_headphones_query
from controllers.db.components.keyboard_controller import insert_keyboard_query
from controllers.db.components.microphone_controller import insert_microphone_query
from controllers.db.components.monitor_controller import insert_monitor_query
from controllers.db.components.motherboard_controller import insert_motherboard_query
from controllers.db.components.mouse_controller import insert_mouse_query
from controllers.db.components.power_supply_controller import insert_power_supply_query
from controllers.db.components.ram_controller import insert_ram_query
from controllers.db.components.storage_controller import insert_storage_query

from database.psql import get_psql_db_connection

from logger_settings import setup_logger

from enum import StrEnum

logger = setup_logger("components")

class ComponentType(StrEnum):
    cpu = 'cpu'
    motherboard = 'motherboard'
    gpu = 'gpu'
    ram = 'ram'
    case = 'case'
    headphones = 'headphones'
    keyboard = 'keyboard'
    mouse = 'mouse'
    microphone = 'microphone'
    monitor = 'monitor'
    storage = 'storage'
    power_supply = 'power_supply'
    
logger = setup_logger("Запуск component_controller")

def add_component(component_type: ComponentType, price: int, info: dict):
    logger.info("Запуску <add_component>")
    logger.info(
        f"Попытка добавить комплектущую\n"
        f"Тип: {component_type}, цена: {price}\n"
        f"Данные:\n {info}"
    )
    conn = get_psql_db_connection()
    cur = conn.cursor()
    
    try:
        logger.debug(f"Добавляем {component_type}...")
        cur.execute(
            "INSERT INTO components (type, price)"
            "VALUES (%s, %s) RETURNING id;",
            (component_type, price)
        )
        logger.debug(f"Добавили в components")
        component_id = cur.fetchone()[0]                         
        
        insert_queries = {
            ComponentType.cpu: insert_cpu_query,
            ComponentType.motherboard: insert_motherboard_query,
            ComponentType.gpu: insert_gpu_query,
            ComponentType.ram: insert_ram_query,
            ComponentType.case: insert_case_query,
            ComponentType.headphones: insert_headphones_query,
            ComponentType.keyboard: insert_keyboard_query,
            ComponentType.mouse: insert_mouse_query,
            ComponentType.microphone: insert_microphone_query,
            ComponentType.monitor: insert_monitor_query,
            ComponentType.storage: insert_storage_query,
            ComponentType.power_supply: insert_power_supply_query
        }
        logger.debug(f"Добавляем в {component_type}...")
        if component_type in insert_queries:
            query, params = insert_queries[component_type](component_id, info)
            cur.execute(query, params)
            logger.debug(f"{component_type} добавлена!")
        else:
            logger.error(f"Неизвестный тип комплектующей: {type}")
            raise ValueError(f"Неизвестный тип комплектующей: {type}")
        
        conn.commit()
        logger.info(f"{component_type} добавлена")
        return component_id
    except Exception as e:
        conn.rollback()
        logger.error(f"Ошибка при добавлении комплектующей: {e}")
        return None
    finally:
        cur.close()
        conn.close()
