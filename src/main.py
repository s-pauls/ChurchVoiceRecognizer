from config import TARGET_MIC_NAME, PATH_TO_MODEL, get_trigger_phrases_for_service, get_service_name
from audio_device import choose_device_by_name, choose_device_interactively
from recognizer import VoiceRecognizer
from logger import setup_logger
from gui import show_settings_dialog
from settings import load_settings, save_settings
import sounddevice as sd

logger = setup_logger()


def get_device_name_by_index(device_index: int) -> str:
    """Получает название устройства по его индексу"""
    try:
        devices = sd.query_devices()
        return devices[device_index]['name']
    except (IndexError, KeyError):
        return "Неизвестное устройство"


def main():
    logger.info("Запуск системы распознавания речи")
    
    # Загружаем сохраненные настройки
    saved_settings = load_settings()
    device_index = saved_settings.get("audio_device_index")
    service_type = saved_settings.get("service_type", "литургия")
    
    # Проверяем, есть ли сохраненное устройство и действительно ли оно
    if device_index is not None:
        try:
            # Проверяем, доступно ли сохраненное устройство
            devices = sd.query_devices()
            if device_index < len(devices) and devices[device_index]['max_input_channels'] > 0:
                logger.info(f"Использую сохраненное устройство: {device_index} - {devices[device_index]['name']}")
                logger.info(f"Тип службы: {get_service_name(service_type)}")
            else:
                logger.warning("Сохраненное устройство недоступно, показываю диалог настроек")
                device_index = None
        except Exception as e:
            logger.warning(f"Ошибка при проверке сохраненного устройства: {e}")
            device_index = None
    
    # Если нет сохраненного устройства или оно недоступно, показываем GUI
    if device_index is None:
        logger.info("Показываю диалог настроек")
        result = show_settings_dialog()
        
        if result is None:
            logger.info("Пользователь отменил настройку")
            return
            
        device_index, service_type = result
        device_name = get_device_name_by_index(device_index)
        
        # Сохраняем выбранные настройки
        if save_settings(device_index, device_name, service_type):
            logger.info("Настройки сохранены")
        else:
            logger.warning("Не удалось сохранить настройки")

    logger.info(f"Выбран микрофон: index {device_index}")
    logger.info(f"Тип службы: {get_service_name(service_type)}")
    
    # Получаем триггерные фразы для выбранного типа службы
    trigger_phrases = get_trigger_phrases_for_service(service_type)
    logger.info(f"Загружены триггерные фразы: {list(trigger_phrases.keys())}")
    
    # Создаем и запускаем распознавание
    recognizer = VoiceRecognizer(
        model_path=PATH_TO_MODEL, 
        device_index=device_index, 
        logger=logger,
        trigger_phrases=trigger_phrases
    )
    recognizer.listen()


if __name__ == "__main__":
    main()
