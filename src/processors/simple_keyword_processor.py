from typing import List, Dict

class SimpleKeywordProcessor:
    """Простой процессор, который ищет ключевые слова в распознанном тексте."""

    def __init__(self, logger, keywords: List[str]):
        self.logger = logger
        self.keywords = [kw.lower() for kw in keywords]
        self.detected_count = {kw: 0 for kw in self.keywords}

    def process_phrase(self, text: str) -> bool:
        """Обрабатывает фразу, ища в ней ключевые слова."""
        text_lower = text.lower()

        for keyword in self.keywords:
            if keyword in text_lower:
                self.detected_count[keyword] += 1
                self.logger.info(f"🔑 Обнаружено ключевое слово '{keyword}' (раз: {self.detected_count[keyword]})")

        return False

    def get_statistics(self) -> Dict[str, int]:
        """Возвращает статистику обнаруженных ключевых слов."""
        return self.detected_count.copy()

    def reset_statistics(self):
        """Сбрасывает статистику."""
        self.detected_count = {kw: 0 for kw in self.keywords}