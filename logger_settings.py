import logging
import os

def setup_logger(logs_name: str):
    # Указываем путь к файлу логов
    log_file = os.path.join("logs", f"{logs_name}.log")

    # Настраиваем логгер
    logger = logging.getLogger(f"{logs_name}_logger")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, mode="w")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
