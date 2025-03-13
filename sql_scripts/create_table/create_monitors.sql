CREATE TABLE monitors (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    screen_size DECIMAL NOT NULL,
    resolution VARCHAR NOT NULL,
    refresh_rate INT NULL,
    panel_type VARCHAR NULL,
    response_time DECIMAL NULL,
    g_sync BOOLEAN,
    freesync BOOLEAN
);