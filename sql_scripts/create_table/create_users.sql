-- Таблица пользователей
DROP TABLE IF EXISTS users;
-- CREATE TYPE user_role AS ENUM ('user', 'admin', 'guest');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    role user_role DEFAULT 'user' NOT NULL
);


