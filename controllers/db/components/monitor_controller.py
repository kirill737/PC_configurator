def insert_monitor_query(component_id: str, info: dict):
    return ("INSERT INTO monitors (component_id, name, brand, screen_size, resolution, refresh_rate, panel_type, response_time, g_sync, freesync)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (component_id, info['name'], info['brand'], info['screen_size'],
                info['resolution'], info['refresh_rate'], info['panel_type'],
                info['response_time'], info['g_sync'], info['freesync']))
