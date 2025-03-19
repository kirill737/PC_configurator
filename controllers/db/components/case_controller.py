def insert_case_query(component_id: str, info: dict):
    return ("INSERT INTO cases (component_id, name, brand, form_factor, max_gpu_length, max_cpu_cooler_height, max_psu_length)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (component_id, info['name'], info['brand'], info['form_factor'],
                info['max_gpu_length'], info['max_cpu_cooler_height'], info['max_psu_length']))
