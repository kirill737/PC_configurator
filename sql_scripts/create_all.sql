-- Таблица пользователей
DROP TABLE IF EXISTS users;
-- CREATE TYPE user_role AS ENUM ('user', 'admin', 'guest');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash BYTEA NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    role user_role DEFAULT 'user' NOT NULL
);

CREATE TABLE builds (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
    -- FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


-- Таблица комплектующих
CREATE TABLE components (
    id SERIAL PRIMARY KEY,
    type COMPONENT NOT NULL,
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE build_components (
    id SERIAL PRIMARY KEY,
    build_id INT REFERENCES builds(id) ON DELETE CASCADE,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    amount INT NOT NULL DEFAULT 1
);

CREATE TABLE cases (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    form_factor VARCHAR NULL,
    max_gpu_length INT,
    max_cpu_cooler_height INT,
    max_psu_length INT
);

CREATE TABLE cpus (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    cores INT NULL,
    threads INT NULL,
    base_clock DECIMAL NULL,
    boost_clock DECIMAL,
    socket VARCHAR NULL,
    tdp INT NULL
);

CREATE TABLE gpus (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    memory_size INT NULL,
    memory_type VARCHAR NULL,
    core_clock DECIMAL NULL,
    boost_clock DECIMAL,
    tdp INT NULL,
    interface VARCHAR NULL
);

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

CREATE TABLE mice (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NOT NULL,
    dpi INT NULL,
    connection_type CONNECTION_TYPE NOT NULL,
    buttons INT NULL,
    weight DECIMAL,
    rgb BOOLEAN
);

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

CREATE TABLE monitors (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
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

CREATE TABLE motherboards (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    socket VARCHAR NULL,
    chipset VARCHAR NULL,
    form_factor VARCHAR NULL,
    ram_slots INT NULL,
    max_ram INT NULL,
    m2_slots INT
);

CREATE TABLE power_supplies (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    wattage INT NULL,
    efficiency_rating VARCHAR,
    modular BOOLEAN NULL
);

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

CREATE TABLE storages (
    id SERIAL PRIMARY KEY,
    component_id INT REFERENCES components(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    type VARCHAR CHECK (type IN ('SSD', 'HDD')) NOT NULL,
    capacity INT NOT NULL,
    interface VARCHAR NULL,
    read_speed INT,
    write_speed INT
);

CREATE TABLE wishlists (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
    -- FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE wishlist_items (
    id SERIAL PRIMARY KEY,
    wishlist_id INT REFERENCES wishlists(id) ON DELETE CASCADE,
    component_type COMPONENT NOT NULL,
    component_id INT NOT NULL
);
