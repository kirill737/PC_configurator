from components.case_controller import insert_case_query
from components.cpu_controller import insert_cpu_query
from components.gpu_controller import insert_gpu_query
from components.headphones_controller import insert_headphones_query
from components.keyboard_controller import insert_keyboard_query
from components.microphone_controller import insert_microphone_query
from components.monitor_controller import insert_monitor_query
from components.motherboard_controller import insert_motherboard_query
from components.mouse_controller import insert_mouse_query
from components.power_supply_controller import insert_power_supply_query
from components.ram_controller import insert_ram_query
from components.storage_controller import insert_storage_query

from database.psql import get_psqsl_db_connection

def add_component(component_type: str, price: int, info: dict):
    conn = get_psqsl_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("INSERT INTO components (type, price) VALUES (%s, %s) RETURNING id", (type, price))
        component_id = cur.fetchone()[0]                         
        
        insert_queries = {
            'cpu': insert_cpu_query,
            'motherboard': insert_motherboard_query,
            'gpu': insert_gpu_query,
            'ram': insert_ram_query,
            'case': insert_case_query,
            'headphones': insert_headphones_query,
            'keyboard': insert_keyboard_query,
            'mouse': insert_mouse_query,
            'microphone': insert_microphone_query,
            'monitor': insert_monitor_query,
            'storage': insert_storage_query,
            'power_supply': insert_power_supply_query
        }
        
        if component_type in insert_queries:
            query, params = insert_queries[component_type](component_id, info)
            cur.execute(query, params)
        else:
            raise ValueError(f"Неизвестный тип комплектующей: {type}")
        
        conn.commit()
        return component_id
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при добавлении комплектующей: {e}")
        return None
    finally:
        cur.close()
        conn.close()
