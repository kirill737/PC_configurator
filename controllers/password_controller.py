import bcrypt

def hash_password(raw_password: str) -> str:
    """Хеширует пароль с использованием bcrypt."""
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(raw_password.encode(), salt)
    return password_hash.decode()

def check_password(raw_password: str, password_hash: str) -> bool:
    """Проверяет, соответствует ли пароль его хешу."""
    return bcrypt.checkpw(raw_password.encode(), password_hash.encode())

# Пример использования
hashed = hash_password("my_secure_password")
print(hashed)

# Пример проверки
is_valid = check_password("my_secure_password", hashed)
print(is_valid)



