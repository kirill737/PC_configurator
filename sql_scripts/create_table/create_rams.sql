CREATE TABLE rams (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    capacity INT NULL,
    type VARCHAR NULL,
    speed INT NULL,
    cas_latency INT NULL
);