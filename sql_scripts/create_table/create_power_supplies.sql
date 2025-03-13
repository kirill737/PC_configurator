CREATE TABLE power_supplies (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    wattage INT NULL,
    efficiency_rating VARCHAR,
    modular BOOLEAN NULL
);