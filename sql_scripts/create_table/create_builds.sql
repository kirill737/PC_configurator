CREATE TABLE builds (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS components;
-- Таблица комплектующих
CREATE TABLE components (
    id SERIAL PRIMARY KEY,
    type COMPONENT NOT NULL,
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE build_components (
    id SERIAL PRIMARY KEY,
    build_id INT NOT NULL,
    component_id INT NOT NULL,
    amount INT NOT NULL DEFAULT 1
);
