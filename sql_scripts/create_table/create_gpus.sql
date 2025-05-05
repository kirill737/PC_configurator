CREATE TABLE gpus (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    memory_size INT NULL,
    memory_type VARCHAR NULL,
    core_clock DECIMAL NULL,
    boost_clock DECIMAL,
    tdp INT NULL,
    interface VARCHAR NULL
);