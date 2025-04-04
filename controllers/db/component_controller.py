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
logger.info("Запуска логов componen_controller")

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
    
    cpu_rus = 'процессор'
    motherboard_rus = 'материнская плата'
    gpu_rus = 'видеокарта'
    ram_rus = 'оперативная память'
    case_rus = 'корпус'
    headphones_rus = 'наушники'
    keyboard_rus = 'клавиатура'
    mouse_rus = 'мышь'
    microphone_rus = 'микрофон'
    monitor_rus = 'монитор'
    storage_rus = 'накопитель'
    power_supply_rus = 'блок питания'

type2table_dict = {
    ComponentType.cpu: 'cpus',
    ComponentType.motherboard: 'motherboards',
    ComponentType.gpu: 'gpus',
    ComponentType.ram: 'rams',
    ComponentType.case: 'cases',
    ComponentType.headphones: 'headphones',
    ComponentType.keyboard: 'keyboards',
    ComponentType.mouse: 'mice',
    ComponentType.microphone: 'microphones',
    ComponentType.monitor: 'monitors',
    ComponentType.storage: 'storages',
    ComponentType.power_supply: 'power_supplies'  
}

type2fields_rus_dict = {
    ComponentType.cpu: [
        "название", "бренд", 
        "кол-во ядер", "потоки", "базовая частота", 
        "максимальная частота", "сокет", "теплопакет"
    ],
    ComponentType.gpu: [
        "название", "бренд", "объем памяти", 
        "тип памяти", "базовая частота", "максимальная частота", 
        "теплопакет", "интерфейс"
    ],
    ComponentType.motherboard: [
        "название", "бренд", "сокет", 
        "чипсет", "форм-фактор", "кол-во слотов ram", 
        "макс память", "слоты m2"
    ],
    ComponentType.ram: [
        "название", "бренд", "объем", 
        "тип", "частота", "задержка cas"
    ],
    ComponentType.storage: [
        "название", "бренд", "тип", 
        "объем", "интерфейс", 
        "скорость чтения", "скорость записи"
    ],
    ComponentType.power_supply: [
        "название", "бренд", "мощность", 
        "класс эффективности", "модульный"
    ],
    ComponentType.case: [
        "название", "бренд", "форм-фактор", 
        "макс длина видеокарты", "макс высота кулера", 
        "макс длина блока питания"
    ],
    ComponentType.headphones: [
        "название", "бренд", "тип подключения", 
        "диапазон частот", "микрофон", "подсветка"
    ],
    ComponentType.keyboard: [
        "название", "бренд", "тип свитчей", 
        "тип подключения", "раскладка", "подсветка", 
        "цифровой блок"
    ],
    ComponentType.mouse: [
        "название", "бренд", "dpi", 
        "тип подключения", "кнопки", 
        "вес", "подсветка"
    ],
    ComponentType.microphone: [
        "название", "бренд", "тип подключения", 
        "направленность", "частота дискретизации", 
        "глубина битности"
    ],
    ComponentType.monitor: [
        "название", "бренд", "диагональ экрана", 
        "разрешение", "частота обновления", 
        "тип матрицы", "время отклика", 
        "g sync", "freesync"
    ]
}

type2fields_dict = {
    ComponentType.cpu: [
        "name", "brand", 
        "cores", "threads", "base_clock", 
        "boost_clock", "socket","tdp"
        ],
    ComponentType.gpu: [
        "name", "brand", "memory_size", 
        "memory_type", "core_clock", "boost_clock", 
        "tdp", "interface"
        ],
    ComponentType.motherboard: [
        "name", "brand", "socket", 
        "chipset", "form_factor", "ram_slots", 
        "max_ram", "m2_slots"
        ],
    ComponentType.ram: [
        "name", "brand", "capacity", 
        "type", "speed", "cas_latency"
        ],
    ComponentType.storage: [
        "name", "brand", "type", 
        "capacity", "interface", 
        "read_speed", "write_speed"
        ],
    ComponentType.power_supply: [
        "name", "brand", "wattage", 
        "efficiency_rating", "modular"
        ],
    ComponentType.case: [
        "name", "brand", "form_factor", 
        "max_gpu_length", "max_cpu_cooler_height", 
        "max_psu_length"
        ],
    ComponentType.headphones: [
        "name", "brand", "connection_type", 
        "frequency_range", "microphone", "rgb"
        ],
    ComponentType.keyboard: [
        "name", "brand", "switch_type", 
        "connection_type", "layout", "rgb", 
        "num_pad"
        ],
    ComponentType.mouse: [
        "name", "brand", "dpi", 
        "connection_type", "buttons", 
        "weight", "rgb"
        ],
    ComponentType.microphone: [
        "name", "brand", "connection_type", 
        "directionality", "sample_rate", 
        "bit_depth"
        ],
    ComponentType.monitor: [
        "name", "brand", "screen_size", 
        "resolution", "refresh_rate", 
        "panel_type", "response_time", 
        "g_sync", "freesync"
        ]
} 

type2rus = {
    ComponentType.cpu: ComponentType.cpu_rus,
    ComponentType.motherboard: ComponentType.motherboard_rus,
    ComponentType.gpu: ComponentType.gpu_rus,
    ComponentType.ram: ComponentType.ram_rus,
    ComponentType.case: ComponentType.case_rus,
    ComponentType.headphones: ComponentType.headphones_rus,
    ComponentType.keyboard: ComponentType.keyboard_rus,
    ComponentType.mouse: ComponentType.mouse_rus,
    ComponentType.microphone: ComponentType.microphone_rus,
    ComponentType.monitor: ComponentType.monitor_rus,
    ComponentType.storage: ComponentType.storage_rus,
    ComponentType.power_supply: ComponentType.power_supply_rus
}

def get_component_data(component_id):
    logger.info("Запуск <get_component_data>")
    logger.info(f"Получение данные детали с id: {component_id}")
    
    conn = get_psql_db_connection()
    cur = conn.cursor()
    
    try:
        logger.info(f"Попытка получить поля комплектующей {component_id}...")
        cur.execute(
            "SELECT type FROM components "
            f"WHERE id={component_id};"
        )
        component_type = ComponentType(cur.fetchone()[0])
        component_table = type2table_dict[component_type]
        cur.execute(
            f"SELECT * FROM {component_table} "
            f"WHERE component_id={component_id} "
            "LIMIT 1;"
        )
        
        fields = cur.fetchone()
        result = {}
        i = 1
        for field_name in type2fields_dict[component_type]:
            result[field_name] = fields[i + 1] 
            
            i += 1
        return result
    except Exception as e:
        logger.error(f"Ошибка при получении данных {component_id}: {e}")        
    finally:
        cur.close()
        conn.close()
    
def get_all_component_by_type(ct: ComponentType):
    logger.info("Запусу <get_all_component_by_type>")
    logger.info(f"Получение всех деталей типа {ct}")
    
    conn = get_psql_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            f"SELECT name, component_id FROM {type2table_dict[ct]}")
        raw_components = cur.fetchall()
        logger.debug(raw_components)
        result = []
        for component in raw_components:
            result.append(
                {
                    'name': component[0],
                    'id': component[1]
                }
            )
        return result
        
    except Exception as e:
        logger.error(f"Ошибка при получении комплектующих: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def prepareType(ct: ComponentType):
    return type2rus[ComponentType(ct)].capitalize()

def get_components_fields(component_id: int):
    logger.debug("Запуск функции <get_components_fields>")
    logger.info(f"Получение полей комплектующей {component_id}")
    
    conn = get_psql_db_connection()
    cur = conn.cursor()
    
    try:
        logger.info(f"Попытка получить поля комплектующей {component_id}...")
        cur.execute(
            "SELECT * FROM components "
            f"WHERE id={component_id};"
        )
        component_type = ComponentType(cur.fetchone()[1])
        component_table = type2table_dict[component_type]
        cur.execute(
            f"SELECT * FROM {component_table} "
            f"WHERE component_id={component_id};"
        )
        
        fields = cur.fetchone()
        result = []
        i = 1
        for field_name in type2fields_rus_dict[component_type]:
            result.append (
                {
                    'name': field_name.capitalize(),
                    'value': fields[i + 1]
                }
            )
            
            i += 1
        return result
    except Exception as e:
        logger.error(f"Ошибка при получении полей {component_id}: {e}")        
    finally:
        cur.close()
        conn.close()

def add_component(component_type: ComponentType, price: int, info: dict) -> int:
    logger.debug("Запуску <add_component>")
    logger.info(
        f"Попытка добавить комплектущую\n"
        f"Тип: {component_type}, цена: {price}\n"
        f"Данные:\n {info}"
    )
    conn = get_psql_db_connection()
    cur = conn.cursor()
    
    try:
        logger.debug(f"Добавляем {component_type} в components...")
        cur.execute(
            "INSERT INTO components (type, price)"
            "VALUES (%s, %s) RETURNING id;",
            (component_type, price)
        )
        logger.debug(f"Добавили {component_type} в components!")
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
        
        logger.debug(f"Добавляем в таблицу с {component_type}...")
        if component_type in insert_queries:
            query, params = insert_queries[component_type](component_id, info)
            cur.execute(query, params)
            logger.debug(f" '{component_type}' добавлена!")
        else:
            logger.error(f"Неизвестный тип комплектующей: {component_type}")
            raise ValueError(f"Неизвестный тип комплектующей: {component_type}")
        
        conn.commit()
        logger.info(f"{component_type} добавлена!")
        return component_id
    except Exception as e:
        conn.rollback()
        logger.error(f"Ошибка при добавлении комплектующей: {e}")
        return None
    finally:
        cur.close()
        conn.close()
