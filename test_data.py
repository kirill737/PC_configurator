from controllers.db.component_controller import ComponentType

cpu_info = {
    "name": "Intel Core I5",
    "brand": "Intel",
    "cores": 5,
    "threads": 16,
    "base_clock": 10,
    "boost_clock": 100,
    "socket": "s1",
    "tdp": 1000
}

gpu_info = {
    "name": "NVIDIA RTX 4080",
    "brand": "NVIDIA",
    "memory_size": 16,
    "memory_type": "ANY",
    "core_clock": 2200,
    "boost_clock": 2500,
    "tdp": 320,
    "interface": "PCIe 4.0"
}

motherboard_info = {
    "name": "ASUS ROG Strix B550-F",
    "brand": "ASUS",
    "socket": "AM4",
    "chipset": "B550",
    "form_factor": "ATX",
    "ram_slots": 4,
    "max_ram": 128,
    "m2_slots": 2
}

ram_info = {
    "name": "Corsair Vengeance RGB Pro",
    "brand": "Corsair",
    "capacity": 16,
    "type": "DDR4",
    "speed": 3600,
    "cas_latency": 18
}

storage_info = {
    "name": "Samsung 980 Pro",
    "brand": "Samsung",
    "type": "SSD",
    "capacity": 1000,
    "interface": "NVMe",
    "read_speed": 7000,
    "write_speed": 5000
}

power_supply_info = {
    "name": "Corsair RM850x",
    "brand": "Corsair",
    "wattage": 850,
    "efficiency_rating": "80+ Gold",
    "modular": True
}

case_info = {
    "name": "NZXT H510",
    "brand": "NZXT",
    "form_factor": "ATX",
    "max_gpu_length": 381,
    "max_cpu_cooler_height": 165,
    "max_psu_length": 200
}

monitor_info = {
    "name": "LG UltraGear 27GN950",
    "brand": "LG",
    "screen_size": 27,
    "resolution": "3840x2160",
    "refresh_rate": 144,
    "panel_type": "IPS",
    "response_time": 1,
    "g_sync": True,
    "freesync": True
}

keyboard_info = {
    "name": "Logitech G Pro X",
    "brand": "Logitech",
    "switch_type": "Mechanical",
    "connection_type": "wireless",
    "layout": "100%",
    "rgb": True,
    "num_pad": True
}

mouse_info = {
    "name": "Razer DeathAdder V2",
    "brand": "Razer",
    "dpi": 20000,
    "connection_type": "wired",
    "buttons": 8,
    "weight": 20.2,
    "rgb": False
}

headphones_info = {
    "name": "SteelSeries Arctis Pro",
    "brand": "SteelSeries",
    "connection_type": "wireless",
    "frequency_range": "10-100",
    "microphone": True,
    "rgb": False
}

microphone_info = {
    "name": "Blue Yeti",
    "brand": "Blue",
    "connection_type": "wired",
    "directionality": "Condenser",
    "sample_rate": 333,
    "bit_depth": 16
}

all_for_build = {
    ComponentType.cpu: cpu_info,
    ComponentType.motherboard: motherboard_info,
    ComponentType.gpu: gpu_info,
    ComponentType.ram: ram_info,
    ComponentType.case: case_info,
    ComponentType.headphones: headphones_info,
    ComponentType.keyboard: keyboard_info,
    ComponentType.mouse: mouse_info,
    ComponentType.microphone: microphone_info,
    ComponentType.monitor: monitor_info,
    ComponentType.storage: storage_info,
    ComponentType.power_supply: power_supply_info
}
price = 1000
for ct, info in all_for_build.items():
    info['price'] = price
    price += 1000 
