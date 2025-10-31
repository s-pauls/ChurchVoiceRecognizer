import voice_recogniz_management as vrm
from actions import action_switch_off_all_mics, shutdown

PRIORITY_COMMANDS = {
    "handle_stop": ["останови распознавание"],
    "handle_mic_off": ["выключи микрофоны"],
    "handle_shutdown": ["выключи компьютер", "ангела хранителя", "ангела-хранителя"],
    "handle_pause": ["пауза"],
    "handle_resume": ["продолжай"]
}


class BaseProcessor:

    def __init__(self, logger):
        self.logger = logger

    def process_phrase(self, text: str) -> bool:
        """Обрабатывает базовые команды."""
        phrase = text.strip().lower()
        for handler_name, commands,  in PRIORITY_COMMANDS.items():
            if any(command in phrase for command in commands):
                self.logger.info(f"Обработка приоритетной команды: {handler_name}")
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
        shutdown()
        self.handle_stop()

    def handle_pause(self):
        # Placeholder: implement pause behavior if needed
        vrm.VoiceRecognizerOnPause = True
        self.logger.info("Установлен флаг паузы распознавания")

    def handle_resume(self):
        vrm.VoiceRecognizerOnPause = False
        self.logger.info("Выключен флаг паузы распознавания")
