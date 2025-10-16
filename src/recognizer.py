import vosk
import sounddevice as sd
import queue
import json
from typing import Callable, Optional


class VoiceRecognizer:
    def __init__(self, model_path, device_index, logger, 
                 phrase_processor: Optional[Callable[[str], None]] = None):
        """
        Инициализирует распознаватель речи.
        
        Args:
            model_path: Путь к модели Vosk
            device_index: Индекс аудио устройства
            logger: Объект логгера
            phrase_processor: Функция для обработки распознанных фраз.
                            Принимает строку (распознанный текст) и ничего не возвращает.
        """
        self.model = vosk.Model(model_path)
        self.device_index = device_index
        self.q = queue.Queue()
        self.rec = vosk.KaldiRecognizer(self.model, 16000)
        self.logger = logger
        self.phrase_processor = phrase_processor

    def _callback(self, indata, frames, time, status):
        if status:
            self.logger.warning(f"Аудио статус: {status}")
        self.q.put(bytes(indata))

    def listen(self):
        """Запускает прослушивание и обработку речи."""
        with sd.RawInputStream(samplerate=16000, blocksize=4000, dtype='int16',
                               channels=1, device=self.device_index, callback=self._callback):
            self.logger.info("Начато прослушивание службы")
            while True:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "").lower()
                    if text.strip():
                        self.logger.info(f"Распознано: {text}")
                        self._process_recognized_text(text)
                else:
                    result = json.loads(self.rec.PartialResult())
                    text = result.get("text", "").lower()
                    if text.strip():
                        self.logger.info(f"Распознано Partial: {text}")
                        # Можно также обработать частичные результаты, если нужно
                        # self._process_recognized_text(text)
    
    def _process_recognized_text(self, text: str):
        """Обрабатывает распознанный текст через callback-функцию."""
        if self.phrase_processor:
            try:
                self.phrase_processor(text)
            except Exception as e:
                self.logger.error(f"Ошибка при обработке фразы '{text}': {e}")
        else:
            self.logger.warning(f"Нет обработчика для фразы: {text}")
