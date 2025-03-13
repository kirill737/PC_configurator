CREATE TABLE gpus (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    memory_size INT NULL,
    memory_type VARCHAR NULL,
    core_clock DECIMAL NULL,
    boost_clock DECIMAL,
    tdp INT NULL,
    interface VARCHAR NULL
);