CREATE TABLE cpus (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    cores INT NULL,
    threads INT NULL,
    base_clock DECIMAL NULL,
    boost_clock DECIMAL,
    socket VARCHAR NULL,
    tdp INT NULL
);