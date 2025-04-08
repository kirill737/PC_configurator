def insert_mouse_query(component_id: str, info: dict):
    return ("INSERT INTO mice (component_id, name, brand, dpi, connection_type, buttons, weight, rgb)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (component_id, info['name'], info['brand'], info['dpi'],
                info['connection_type'], info['buttons'], info['weight'], info['rgb']))
