CREATE TABLE mice (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    brand VARCHAR NOT NULL,
    dpi INT NULL,
    connection_type CONNECTION_TYPE NOT NULL,
    buttons INT NULL,
    weight DECIMAL,
    rgb BOOLEAN
);