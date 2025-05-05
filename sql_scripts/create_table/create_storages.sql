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