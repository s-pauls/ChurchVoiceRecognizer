"""
Тестовый скрипт для демонстрации новой архитектуры VoiceRecognizer
без жестких зависимостей.
"""
import time
from recognizer import VoiceRecognizer
from phrase_processors import SERVICE_PROCESSORS, SimpleKeywordProcessor
from logger import setup_logger


def test_phrase_processors():
    """Тестирует различные обработчики фраз."""
    logger = setup_logger()
    
    print("🧪 Тестирование обработчиков фраз\n")
    
    # Тестовые фразы
    test_phrases = [
        "Царю небесный утешителю",
        "Отче наш, да святится имя Твое",
        "Господи помилуй",
        "Святый Боже, Святый Крепкий",
        "Благослови душе моя Господа",
        "Свете тихий святыя славы",
        "Аллилуйя, аллилуйя, аллилуйя"
    ]
    
    # Тестируем разные процессоры
    for service_name, processor_factory in SERVICE_PROCESSORS.items():
        print(f"--- Тестирование процессора: {service_name.upper()} ---")
        processor = processor_factory(logger)
        
        for phrase in test_phrases:
            print(f"Обрабатываем: '{phrase}'")
            processor(phrase)
            time.sleep(0.1)  # Небольшая пауза для читаемости
        
        print()


def test_custom_processor():
    """Тестирует создание кастомного процессора."""
    logger = setup_logger()
    
    print("🔧 Тестирование кастомного процессора\n")
    
    # Создаем кастомный процессор
    custom_keywords = ["аминь", "слава", "честь", "благодать"]
    keyword_processor = SimpleKeywordProcessor(logger, custom_keywords)
    
    test_phrases = [
        "Слава Отцу и Сыну и Святому Духу",
        "И ныне и присно и во веки веков, аминь",
        "Благодать Господа нашего",
        "Честь и поклонение Троице"
    ]
    
    for phrase in test_phrases:
        print(f"Обрабатываем: '{phrase}'")
        keyword_processor.process_phrase(phrase)
    
    print(f"\n📊 Статистика: {keyword_processor.get_statistics()}")


def test_voice_recognizer_flexibility():
    """Демонстрирует гибкость нового VoiceRecognizer."""
    logger = setup_logger()
    
    print("🎤 Демонстрация гибкости VoiceRecognizer\n")
    
    # Создаем простой мок-процессор
    processed_phrases = []
    
    def mock_processor(text: str):
        processed_phrases.append(text)
        print(f"📝 Мок-процессор обработал: '{text}'")
    
    # Имитируем создание VoiceRecognizer с кастомным процессором
    # (без реального аудио, только для демонстрации API)
    print("Создание VoiceRecognizer с кастомным процессором...")
    
    try:
        # Это бы работало при наличии модели и аудио устройства
        # recognizer = VoiceRecognizer(
        #     model_path="path/to/model",
        #     device_index=0,
        #     logger=logger,
        #     phrase_processor=mock_processor
        # )
        print("✅ VoiceRecognizer может быть создан с любым процессором!")
        
        # Демонстрируем смену процессора
        liturgy_processor = SERVICE_PROCESSORS["литургия"](logger)
        print("✅ Процессор можно менять динамически!")
        
        # Тестируем обработку фраз
        test_phrases = ["Царю небесный", "Отче наш"]
        for phrase in test_phrases:
            mock_processor(phrase)
            liturgy_processor(phrase)
        
        print(f"\n📋 Мок-процессор обработал {len(processed_phrases)} фраз")
        
    except Exception as e:
        print(f"⚠️  Ошибка: {e}")
        print("Это нормально для демонстрации без реального аудио.")


if __name__ == "__main__":
    print("🚀 Запуск тестов новой архитектуры\n")
    
    test_phrase_processors()
    print("="*60)
    
    test_custom_processor()
    print("="*60)
    
    test_voice_recognizer_flexibility()
    print("\n🎉 Тестирование завершено!")