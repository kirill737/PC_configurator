def insert_ram_query(component_id: str, info: dict):
    return ("INSERT INTO rams (component_id, name, brand, capacity, type, speed, cas_latency)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (component_id, info['name'], info['brand'], info['capacity'], info['type'],
                info['speed'], info['cas_latency']))