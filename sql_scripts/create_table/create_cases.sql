CREATE TABLE cases (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    brand VARCHAR NULL,
    form_factor VARCHAR NULL,
    max_gpu_length INT,
    max_cpu_cooler_height INT,
    max_psu_length INT
);