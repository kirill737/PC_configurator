def insert_keyboard_query(component_id: str, info: dict):
    return ("INSERT INTO keyboards (component_id, name, brand, switch_type, connection_type, layout, rgb, num_pad)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (component_id, info['name'], info['brand'], info['switch_type'],
                info['connection_type'], info['layout'], info['rgb'], info['num_pad']))
