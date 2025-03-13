CREATE TABLE motherboards (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    socket VARCHAR NULL,
    chipset VARCHAR NULL,
    form_factor VARCHAR NULL,
    ram_slots INT NULL,
    max_ram INT NULL,
    m2_slots INT
);