CREATE TABLE cpus (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    cores INT NULL,
    threads INT NULL,
    base_clock DECIMAL NULL,
    boost_clock DECIMAL,
    socket VARCHAR NULL,
    tdp INT NULL
); 