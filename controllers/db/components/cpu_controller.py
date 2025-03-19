def insert_cpu_query(component_id: str, info: dict):
    return ("INSERT INTO cpus (component_id, name, brand, cores, threads, base_clock, boost_clock, socket, tdp)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (component_id, info['name'], info['brand'], info['cores'], info['threads'],
                info['base_clock'], info['boost_clock'], info['socket'], info['tdp']))