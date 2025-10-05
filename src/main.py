from config import TARGET_MIC_NAME, PATH_TO_MODEL
from audio_device import choose_device_by_name, choose_device_interactively
from recognizer import VoiceRecognizer
from logger import setup_logger

logger = setup_logger()


def main():
    logger.info("Запуск системы распознавания речи")

    device_index = choose_device_by_name(TARGET_MIC_NAME) if TARGET_MIC_NAME else None
    if device_index is None:
        logger.info("Имя микрофона не задано — переходим к ручному выбору")
        device_index = choose_device_interactively()

    logger.info(f"Выбран микрофон: index {device_index}")
    recognizer = VoiceRecognizer(model_path=PATH_TO_MODEL, device_index=device_index, logger=logger)
    recognizer.listen()


if __name__ == "__main__":
    main()
