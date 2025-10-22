import logging
import os


def setup_logger(name="voice_trigger", log_file="voice_trigger.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s — %(levelname)s — %(message)s')

    # Создаем папку logs, если её нет
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Полный путь к файлу лога
    log_file_path = os.path.join(logs_dir, log_file)
    
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
