CREATE TABLE power_supplies (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    wattage INT NULL,
    efficiency_rating VARCHAR,
    modular BOOLEAN NULL
);