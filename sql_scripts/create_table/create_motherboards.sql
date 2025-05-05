CREATE TABLE motherboards (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    socket VARCHAR NULL,
    chipset VARCHAR NULL,
    form_factor VARCHAR NULL,
    ram_slots INT NULL,
    max_ram INT NULL,
    m2_slots INT
);