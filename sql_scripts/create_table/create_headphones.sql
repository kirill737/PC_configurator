CREATE TABLE headphones (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    connection_type CONNECTION_TYPE NOT NULL,
    frequency_range VARCHAR,
    microphone BOOLEAN,
    rgb BOOLEAN
);