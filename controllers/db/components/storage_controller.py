def insert_storage_query(component_id: str, info: dict):
    return ("INSERT INTO storages (component_id, name, brand, type, capacity, interface, read_speed, write_speed)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (component_id, info['name'], info['brand'], info['type'],
                info['capacity'], info['interface'], info['read_speed'], info['write_speed']))
