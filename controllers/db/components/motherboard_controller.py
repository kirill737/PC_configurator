def insert_motherboard_query(component_id: str, info: dict):
    return ("INSERT INTO motherboards (component_id, name, brand, socket, chipset, form_factor, ram_slots, max_ram, m2_slots)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (component_id, info['name'], info['brand'], info['socket'], info['chipset'],
                info['form_factor'], info['ram_slots'], info['max_ram'], info['m2_slots']))