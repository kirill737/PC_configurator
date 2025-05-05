import logging
import os

def setup_logger(logs_name: str):
    # Указываем путь к файлу логов
    log_file = os.path.join("logs", f"{logs_name}.log")
    main_log_file = os.path.join("logs", "main_log.log")

    # Настраиваем логгер
    logger = logging.getLogger(f"{logs_name}_logger")
    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, mode="w")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%H:%M:%S")
    file_handler.setFormatter(formatter)

    # Обработчик для основного лога (main_log)
    main_log_handler = logging.FileHandler(main_log_file, mode="a")
    main_log_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(main_log_handler)

    # Открытие файла в режиме записи ('w') для очистки его содержимого
    with open("./logs/main_log.log", "w"):
        pass

    return logger
