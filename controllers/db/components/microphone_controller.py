def insert_microphone_query(component_id: str, info: dict):
    return ("INSERT INTO microphones (component_id, name, brand, connection_type, directionality, sample_rate, bit_depth)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (component_id, info['name'], info['brand'], info['connection_type'],
                info['directionality'], info['sample_rate'], info['bit_depth']))
