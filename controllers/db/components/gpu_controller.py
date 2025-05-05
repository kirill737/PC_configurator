def insert_gpu_query(component_id: str, info: dict):
    return ("INSERT INTO gpus (component_id, name, brand, memory_size, memory_type, core_clock, boost_clock, tdp, interface)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (component_id, info['name'], info['brand'], info['memory_size'], info['memory_type'],
                info['core_clock'], info['boost_clock'], info['tdp'], info['interface']))