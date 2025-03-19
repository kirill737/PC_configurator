INSERT INTO users (name, email, password_hash, role) VALUES
('kirill737', 'kirill737apple@yandex.ru', DECODE('test_hash'), 'admin'),
('Петр Петров', 'petr@example.com', 'hashed_password_2', 'user'),
('Анна Смирнова', 'anna@example.com', 'hashed_password_3', 'user'),
('Гость', 'guest@example.com', 'hashed_password_4', 'guest'),
('Мария Сидорова', 'maria@example.com', 'hashed_password_5', 'user');
