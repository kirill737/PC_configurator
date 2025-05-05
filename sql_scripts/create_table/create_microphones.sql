CREATE TABLE microphones (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    connection_type CONNECTION_TYPE NOT NULL,
    directionality VARCHAR NULL,
    sample_rate INT NULL,
    bit_depth INT NULL
);