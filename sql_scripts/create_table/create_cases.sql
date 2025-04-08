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