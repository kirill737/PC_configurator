CREATE TABLE keyboards (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    switch_type VARCHAR NULL,
    connection_type CONNECTION_TYPE NOT NULL,
    layout KEYBOARD_LAYOUT NOT NULL,
    rgb BOOLEAN,
    num_pad BOOLEAN
);