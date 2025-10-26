import voice_recogniz_management as vrm
import datetime
import time
from config import PATH_TO_MODEL, SERVICE_WAIT_ENABLED, SERVICE_SCHEDULE
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

    base_processor_def = SERVICE_PROCESSORS.get("базовый")

    if base_processor_def:
        base_processor = base_processor_def(logger)
        logger.info("Инициализирован базовый процессор")

    # Создаем обработчик фраз в зависимости от типа службы
    processor_factory = SERVICE_PROCESSORS.get(service_type.lower())
    
    if processor_factory:
        phrase_processor = processor_factory(logger)
        logger.info(f"Инициализирован процессор для службы: {service_type}")

    def combined_processor(text: str) -> bool:
        if base_processor(text):
            return True

        if not vrm.VoiceRecognizerOnPause:
            return phrase_processor(text)

        return False

    # Создаем и запускаем распознавание
    recognizer = VoiceRecognizer(
        model_path=PATH_TO_MODEL, 
        device_index=device_index, 
        logger=logger,
        phrase_processor=combined_processor
    )

    # Ожидаем до времени начала службы
    wait_until_service_time()

    recognizer.listen()


def wait_until_service_time():
    """Ожидает до времени начала службы в зависимости от дня недели"""
    if not SERVICE_WAIT_ENABLED:
        logger.info("Ожидание до времени службы отключено в настройках")
        return
        
    now = datetime.datetime.now()
    weekday = now.weekday()  # 0 = понедельник, 6 = воскресенье
    
    # Получаем настройки службы для текущего дня недели
    service_config = SERVICE_SCHEDULE.get(weekday)
    if not service_config:
        logger.warning(f"Не найдены настройки службы для дня недели {weekday}")
        return
    
    hour, minute, service_name = service_config
    service_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    # Если время уже прошло, не ждем
    if now >= service_time:
        logger.info(f"Время {service_name} службы ({service_time.strftime('%H:%M')}) уже наступило")
        return
    
    # Вычисляем время ожидания
    wait_seconds = (service_time - now).total_seconds()
    logger.info(f"Ожидание до начала {service_name} службы ({service_time.strftime('%H:%M')}). "
               f"Осталось: {int(wait_seconds // 60)} мин {int(wait_seconds % 60)} сек")
    
    time.sleep(wait_seconds)
    logger.info(f"Время {service_name} службы наступило!")
    

if __name__ == "__main__":
    main()
