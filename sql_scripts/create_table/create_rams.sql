CREATE TABLE rams (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    capacity INT NULL,
    type VARCHAR NULL,
    speed INT NULL,
    cas_latency INT NULL
);