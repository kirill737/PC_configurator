from controllers.db.component_controller import ComponentType, add_component

cpu_info = [
    {
        "name": "AMD Ryzen 7 5800X",
        "brand": "AMD",
        "cores": 8,
        "threads": 16,
        "base_clock": 3.8,
        "boost_clock": 4.7,
        "socket": "AM4",
        "tdp": 105
    },
    {
        "name": "Intel Core i7-12700K",
        "brand": "Intel",
        "cores": 12,
        "threads": 20,
        "base_clock": 3.6,
        "boost_clock": 5.0,
        "socket": "LGA1700",
        "tdp": 125
    },
    {
        "name": "AMD Ryzen 9 7950X",
        "brand": "AMD",
        "cores": 16,
        "threads": 32,
        "base_clock": 4.5,
        "boost_clock": 5.7,
        "socket": "AM5",
        "tdp": 170
    }
]

gpu_info = [
    {
        "name": "AMD Radeon RX 7900 XTX",
        "brand": "AMD",
        "memory_size": 24,
        "memory_type": "GDDR6",
        "core_clock": 2300,
        "boost_clock": 2500,
        "tdp": 355,
        "interface": "PCIe 4.0"
    },
    {
        "name": "NVIDIA RTX 4070 Ti",
        "brand": "NVIDIA",
        "memory_size": 12,
        "memory_type": "GDDR6X",
        "core_clock": 2310,
        "boost_clock": 2610,
        "tdp": 285,
        "interface": "PCIe 4.0"
    },
    {
        "name": "Intel Arc A770",
        "brand": "Intel",
        "memory_size": 16,
        "memory_type": "GDDR6",
        "core_clock": 2100,
        "boost_clock": 2400,
        "tdp": 225,
        "interface": "PCIe 4.0"
    }
]

motherboard_info = [
    {
        "name": "MSI MAG B660M Mortar",
        "brand": "MSI",
        "socket": "LGA1700",
        "chipset": "B660",
        "form_factor": "Micro-ATX",
        "ram_slots": 4,
        "max_ram": 128,
        "m2_slots": 2
    },
    {
        "name": "Gigabyte X570 AORUS Elite",
        "brand": "Gigabyte",
        "socket": "AM4",
        "chipset": "X570",
        "form_factor": "ATX",
        "ram_slots": 4,
        "max_ram": 128,
        "m2_slots": 3
    },
    {
        "name": "ASUS Prime Z790-A",
        "brand": "ASUS",
        "socket": "LGA1700",
        "chipset": "Z790",
        "form_factor": "ATX",
        "ram_slots": 4,
        "max_ram": 192,
        "m2_slots": 4
    }
]

ram_info = [
    {
        "name": "G.Skill Trident Z RGB",
        "brand": "G.Skill",
        "capacity": 32,
        "type": "DDR4",
        "speed": 4000,
        "cas_latency": 18
    },
    {
        "name": "Kingston Fury Beast",
        "brand": "Kingston",
        "capacity": 16,
        "type": "DDR5",
        "speed": 5200,
        "cas_latency": 36
    },
    {
        "name": "Crucial Ballistix",
        "brand": "Crucial",
        "capacity": 64,
        "type": "DDR4",
        "speed": 3200,
        "cas_latency": 16
    }
]

storage_info = [
    {
        "name": "WD Black SN850",
        "brand": "Western Digital",
        "type": "SSD",
        "capacity": 2000,
        "interface": "NVMe",
        "read_speed": 7000,
        "write_speed": 5300
    },
    {
        "name": "Seagate Barracuda",
        "brand": "Seagate",
        "type": "HDD",
        "capacity": 4000,
        "interface": "SATA",
        "read_speed": 200,
        "write_speed": 190
    },
    {
        "name": "Kingston KC3000",
        "brand": "Kingston",
        "type": "SSD",
        "capacity": 1000,
        "interface": "NVMe",
        "read_speed": 7000,
        "write_speed": 6000
    }
]

power_supply_info = [
    {
        "name": "EVGA SuperNOVA 1000 G5",
        "brand": "EVGA",
        "wattage": 1000,
        "efficiency_rating": "80+ Gold",
        "modular": True
    },
    {
        "name": "Be Quiet! Pure Power 11",
        "brand": "Be Quiet!",
        "wattage": 700,
        "efficiency_rating": "80+ Bronze",
        "modular": False
    },
    {
        "name": "Seasonic Focus GX-750",
        "brand": "Seasonic",
        "wattage": 750,
        "efficiency_rating": "80+ Platinum",
        "modular": True
    }
]

case_info = [
    {
        "name": "Fractal Design Meshify C",
        "brand": "Fractal Design",
        "form_factor": "ATX",
        "max_gpu_length": 315,
        "max_cpu_cooler_height": 170,
        "max_psu_length": 200
    },
    {
        "name": "Cooler Master MasterBox NR200",
        "brand": "Cooler Master",
        "form_factor": "Mini-ITX",
        "max_gpu_length": 330,
        "max_cpu_cooler_height": 155,
        "max_psu_length": 130
    },
    {
        "name": "Lian Li PC-O11 Dynamic",
        "brand": "Lian Li",
        "form_factor": "ATX",
        "max_gpu_length": 420,
        "max_cpu_cooler_height": 167,
        "max_psu_length": 210
    }
]

headphones_info = [
    {
        "name": "HyperX Cloud Alpha",
        "brand": "HyperX",
        "connection_type": "wired",
        "frequency_range": "15-25000",
        "microphone": True,
        "rgb": False
    },
    {
        "name": "Razer BlackShark V2 Pro",
        "brand": "Razer",
        "connection_type": "wireless",
        "frequency_range": "12-28000",
        "microphone": True,
        "rgb": True
    },
    {
        "name": "Sony WH-1000XM5",
        "brand": "Sony",
        "connection_type": "wireless",
        "frequency_range": "4-40000",
        "microphone": True,
        "rgb": False
    }
]

keyboard_info = [
    {
        "name": "Razer Huntsman Elite",
        "brand": "Razer",
        "switch_type": "Opto-Mechanical",
        "connection_type": "wired",
        "layout": "100%",
        "rgb": True,
        "num_pad": True
    },
    {
        "name": "SteelSeries Apex Pro",
        "brand": "SteelSeries",
        "switch_type": "Mechanical",
        "connection_type": "wired",
        "layout": "80%",
        "rgb": True,
        "num_pad": False
    },
    {
        "name": "Keychron K6",
        "brand": "Keychron",
        "switch_type": "Mechanical",
        "connection_type": "wireless",
        "layout": "75%",
        "rgb": True,
        "num_pad": False
    }
]

mouse_info = [
    {
        "name": "Logitech G Pro X Superlight",
        "brand": "Logitech",
        "dpi": 25600,
        "connection_type": "wireless",
        "buttons": 5,
        "weight": 63,
        "rgb": False
    },
    {
        "name": "SteelSeries Rival 600",
        "brand": "SteelSeries",
        "dpi": 12000,
        "connection_type": "wired",
        "buttons": 7,
        "weight": 96,
        "rgb": True
    },
    {
        "name": "Glorious Model O",
        "brand": "Glorious",
        "dpi": 19000,
        "connection_type": "wired",
        "buttons": 6,
        "weight": 67,
        "rgb": True
    }
]

microphone_info = [
    {
        "name": "Shure SM7B",
        "brand": "Shure",
        "connection_type": "wired",
        "directionality": "Dynamic",
        "sample_rate": 48000,
        "bit_depth": 24
    },
    {
        "name": "Elgato Wave 3",
        "brand": "Elgato",
        "connection_type": "wired",
        "directionality": "Condenser",
        "sample_rate": 96000,
        "bit_depth": 24
    },
    {
        "name": "RØDE NT-USB",
        "brand": "RØDE",
        "connection_type": "wired",
        "directionality": "Condenser",
        "sample_rate": 44100,
        "bit_depth": 16
    }
]

monitor_info = [
    {
        "name": "ASUS ROG Swift PG259QN",
        "brand": "ASUS",
        "screen_size": 24.5,
        "resolution": "1920x1080",
        "refresh_rate": 360,
        "panel_type": "IPS",
        "response_time": 1,
        "g_sync": True,
        "freesync": False
    },
    {
        "name": "Gigabyte M32U",
        "brand": "Gigabyte",
        "screen_size": 32,
        "resolution": "3840x2160",
        "refresh_rate": 144,
        "panel_type": "IPS",
        "response_time": 1,
        "g_sync": False,
        "freesync": True
    },
    {
        "name": "Samsung Odyssey G9",
        "brand": "Samsung",
        "screen_size": 49,
        "resolution": "5120x1440",
        "refresh_rate": 240,
        "panel_type": "VA",
        "response_time": 1,
        "g_sync": True,
        "freesync": True
    }
]

components = {
        ComponentType.cpu: [],
        ComponentType.motherboard: [],
        ComponentType.gpu: [],
        ComponentType.ram: [],
        ComponentType.case: [],
        ComponentType.headphones: [],
        ComponentType.keyboard: [],
        ComponentType.mouse: [],
        ComponentType.microphone: [],
        ComponentType.monitor: [],
        ComponentType.storage: [],
        ComponentType.power_supply: []  
    }

for i in range(3):
    components[ComponentType.cpu].append(cpu_info[i]),
    components[ComponentType.motherboard].append(motherboard_info[i]),
    components[ComponentType.gpu].append(gpu_info[i]),
    components[ComponentType.ram].append(ram_info[i]),
    components[ComponentType.case].append(case_info[i]),
    components[ComponentType.headphones].append(headphones_info[i]),
    components[ComponentType.keyboard].append(keyboard_info[i]),
    components[ComponentType.mouse].append(mouse_info[i]),
    components[ComponentType.microphone].append(microphone_info[i]),
    components[ComponentType.monitor].append(monitor_info[i]),
    components[ComponentType.storage].append(storage_info[i]),
    components[ComponentType.power_supply].append(power_supply_info[i])
    

        
        
