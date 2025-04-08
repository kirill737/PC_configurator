INSERT INTO cpus (name, brand, cores, threads, base_clock, boost_clock, socket, tdp) VALUES
    ('Ryzen 5 5600X', 'AMD', 6, 12, 3.7, 4.6, 'AM4', 65),
    ('Core i7-12700K', 'Intel', 12, 20, 3.6, 5.0, 'LGA1700', 125);

INSERT INTO motherboards (name, brand, socket, chipset, form_factor, ram_slots, max_ram, m2_slots) VALUES
    ('MSI B450 TOMAHAWK', 'MSI', 'AM4', 'B450', 'ATX', 4, 64, 2),
    ('ASUS ROG STRIX Z690-E', 'ASUS', 'LGA1700', 'Z690', 'ATX', 4, 128, 3);

INSERT INTO gpus (name, brand, memory_size, memory_type, core_clock, boost_clock, tdp, interface) VALUES
    ('RTX 3080', 'NVIDIA', 10, 'GDDR6X', 1440, 1710, 320, 'PCIe 4.0'),
    ('RX 6800 XT', 'AMD', 16, 'GDDR6', 1825, 2250, 300, 'PCIe 4.0');