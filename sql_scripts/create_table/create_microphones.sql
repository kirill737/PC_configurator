CREATE TABLE microphones (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    connection_type CONNECTION_TYPE NOT NULL,
    directionality VARCHAR NULL,
    sample_rate INT NULL,
    bit_depth INT NULL
);