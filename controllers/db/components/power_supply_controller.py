def insert_power_supply_query(component_id: str, info: dict):
    return ("INSERT INTO power_suplies (component_id, name, brand, wattage, efficiency_rating, modular)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (component_id, info['name'], info['brand'], info['wattage'],
                info['efficiency_rating'], info['modular']))
