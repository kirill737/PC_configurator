CREATE TABLE storages (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    type VARCHAR CHECK (type IN ('SSD', 'HDD')) NOT NULL,
    capacity INT NOT NULL,
    interface VARCHAR NULL,
    read_speed INT,
    write_speed INT
);