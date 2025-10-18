import src.voice_recogniz_management as vrm
from src.actions import action_switch_off_all_mics

PRIORITY_COMMANDS = {
    "стоп": "handle_stop",
    "выключи микрофоны": "handle_mic_off",
    "выключи компьютер": "handle_shutdown",
    "пауза": "handle_pause",
    "продолжай": "handle_resume"
}


class BaseProcessor:

    def __init__(self, logger):
        self.logger = logger

    def process_phrase(self, text: str) -> bool:
        """Обрабатывает базовые команды."""
        phrase = text.strip().lower()
        for command, handler_name in PRIORITY_COMMANDS.items():
            if command in phrase:
                self.logger.info(f"Обработка приоритетной команды: {command}")
                handler = getattr(self, handler_name, None)
                if handler:
                    handler()
                return True
        return False

    def handle_stop(self):
        # Set the module-level running flag to False so the recognizer loop can stop.
        vrm.RunningVoiceRecognizer = False
        self.logger.info("Установлен флаг остановки распознавания")

    def handle_mic_off(self):
        action_switch_off_all_mics()

    def handle_shutdown(self):
        self.logger.info("✅ Действие: Выключение компьютера (заглушка)")

    def handle_pause(self):
        # Placeholder: implement pause behavior if needed
        vrm.VoiceRecognizerOnPause = True
        self.logger.info("Установлен флаг паузы распознавания")

    def handle_resume(self):
        vrm.VoiceRecognizerOnPause = False
        self.logger.info("Выключен флаг паузы распознавания")
