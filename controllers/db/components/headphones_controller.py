def insert_headphones_query(component_id: str, info: dict):
    return ("INSERT INTO headphones (component_id, name, brand, connection_type, frequency_range, microphone, rgb)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (component_id, info['name'], info['brand'], info['connection_type'],
                info['frequency_range'], info['microphone'], info['rgb']))
