class VesperProcessor:
    """Обработчик для вечерней службы."""

    def __init__(self, logger):
        self.logger = logger
        self.state = "waiting_start"
        self.psalm_count = 0

    def process_phrase(self, text: str):
        """Обрабатывает фразы вечерней службы."""
        text = text.lower()

        if self.state == "waiting_start":
            if "благослови душе моя господа" in text:
                self.state = "psalm_reading"
                self.logger.info("🌅 Начало вечерней службы")

        elif self.state == "psalm_reading":
            if "псалом" in text:
                self.psalm_count += 1
                self.logger.info(f"📖 Псалом #{self.psalm_count}")

            if "свете тихий" in text:
                self.state = "vesper_prayers"
                self.logger.info("🕯️ Переход к вечерним молитвам")

        elif self.state == "vesper_prayers":
            if "ныне отпущаеши" in text:
                self.state = "service_end"
                self.logger.info("✨ Завершение вечерней службы")

    def reset(self):
        """Сбрасывает состояние процессора."""
        self.state = "waiting_start"
        self.psalm_count = 0