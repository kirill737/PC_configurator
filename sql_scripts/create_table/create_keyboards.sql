CREATE TABLE keyboards (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    switch_type VARCHAR NULL,
    connection_type CONNECTION_TYPE NOT NULL,
    layout KEYBOARD_LAYOUT NOT NULL,
    rgb BOOLEAN,
    num_pad BOOLEAN
);