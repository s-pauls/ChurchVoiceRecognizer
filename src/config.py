TARGET_MIC_NAME = ""  # Если пусто — будет GUI выбор

# Триггерные фразы для разных типов служб
SERVICE_CONFIGS = {
    "литургия": {
        "name": "Божественная Литургия",
        "trigger_phrases": {
            "отче наш": "on_prayer",
            "двери двери": "on_doors",
            "благословенно царство": "on_begin",
            "святый боже": "on_trisagion",
            "херувимская": "on_cherubic",
            "достойно есть": "on_axion"
        }
    },
    "всенощная": {
        "name": "Всенощное бдение",
        "trigger_phrases": {
            "отче наш": "on_prayer",
            "богородице дево": "on_theotokos",
            "хвалите имя": "on_praise",
            "величание": "on_magnification",
            "тропарь": "on_troparion",
            "слава в вышних": "on_gloria"
        }
    }
}

# Триггерные фразы по умолчанию (для обратной совместимости)
TRIGGER_PHRASES = SERVICE_CONFIGS["литургия"]["trigger_phrases"]

PATH_TO_MODEL = "models/vosk-model-small-ru-0.22" # "models/vosk-model-ru-0.42"


def get_trigger_phrases_for_service(service_type: str) -> dict:
    """Возвращает триггерные фразы для указанного типа службы"""
    return SERVICE_CONFIGS.get(service_type, SERVICE_CONFIGS["литургия"])["trigger_phrases"]


def get_service_name(service_type: str) -> str:
    """Возвращает полное название службы"""
    return SERVICE_CONFIGS.get(service_type, SERVICE_CONFIGS["литургия"])["name"]