from config import PATH_TO_MODEL
from recognizer import VoiceRecognizer
from logger import setup_logger
from gui import show_settings_dialog
from settings import save_settings, load_settings
from phrase_processors_factory import SERVICE_PROCESSORS

logger = setup_logger()


def main():
    logger.info("Запуск системы распознавания речи")

    # Показываем GUI
    settings = load_settings()
    saved_device_name = settings.get("audio_device_name")

    logger.info("Показываю диалог настроек")
    result = show_settings_dialog(saved_device_name)

    if result is None:
        logger.info("Пользователь отменил распознавание речи")
        return

    device_index, device_name, service_type = result

    # Сохраняем выбранные настройки
    if save_settings(device_name):
        logger.info("Настройки сохранены")
    else:
        logger.warning("Не удалось сохранить настройки")

    logger.info(f"Выбрана служба: {service_type} с устройством: {device_name}")

    # Создаем обработчик фраз в зависимости от типа службы
    processor_factory = SERVICE_PROCESSORS.get(service_type.lower())
    
    if processor_factory:
        phrase_processor = processor_factory(logger)
        logger.info(f"Инициализирован процессор для службы: {service_type}")
    else:
        # Обработчик по умолчанию для неизвестных типов служб
        def default_processor(text: str):
            logger.info(f"Обработка фразы (по умолчанию): {text}")
        phrase_processor = default_processor
        logger.info(f"Используется обработчик по умолчанию для службы: {service_type}")
        logger.info(f"Доступные типы служб: {list(SERVICE_PROCESSORS.keys())}")

    # Создаем и запускаем распознавание
    recognizer = VoiceRecognizer(
        model_path=PATH_TO_MODEL, 
        device_index=device_index, 
        logger=logger,
        phrase_processor=phrase_processor
    )
    recognizer.listen()


if __name__ == "__main__":
    main()
