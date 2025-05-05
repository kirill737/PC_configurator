CREATE TABLE headphones (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    connection_type CONNECTION_TYPE NOT NULL,
    frequency_range VARCHAR,
    microphone BOOLEAN,
    rgb BOOLEAN
);