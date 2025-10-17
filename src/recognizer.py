import vosk
import sounddevice as sd
import queue
import json
import time
from typing import Callable, Optional
from collections import deque


class VoiceRecognizer:
    def __init__(self, model_path, device_index, logger, 
                 phrase_processor: Optional[Callable[[str], None]] = None,
                 buffer_duration: int = 30,
                 min_phrase_length: int = 3):
        """
        Инициализирует распознаватель речи.
        
        Args:
            model_path: Путь к модели Vosk
            device_index: Индекс аудио устройства
            logger: Объект логгера
            phrase_processor: Функция для обработки распознанных фраз.
                            Принимает строку (распознанный текст) и ничего не возвращает.
            buffer_duration: Время хранения текста в буфере (секунды)
            min_phrase_length: Минимальная длина фразы для обработки (символы)
        """
        self.model = vosk.Model(model_path)
        self.device_index = device_index
        self.q = queue.Queue()
        self.rec = vosk.KaldiRecognizer(self.model, 16000)
        self.logger = logger
        self.phrase_processor = phrase_processor
        
        # Буфер для накопления текста
        self.text_buffer = deque()
        self.buffer_duration = buffer_duration
        self.min_phrase_length = min_phrase_length
        self.last_partial_text = ""
        self.last_activity_time = time.time()

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
                current_time = time.time()
                
                if self.rec.AcceptWaveform(data):
                    # Полный результат распознавания
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "").lower().strip()
                    
                    if text and len(text) >= self.min_phrase_length:
                        self.logger.info(f"Распознано полное: {text}")
                        self._add_to_buffer(text, current_time)
                        self._process_buffer()
                        self.last_partial_text = ""  # Сброс частичного текста
                else:
                    # Частичный результат распознавания
                    result = json.loads(self.rec.PartialResult())
                    partial_text = result.get("partial", "").lower().strip()
                    
                    if partial_text and len(partial_text) >= self.min_phrase_length:
                        # Обрабатываем только если частичный текст существенно изменился
                        if self._is_significant_change(partial_text):
                            self.logger.info(f"Частичное распознавание: {partial_text}")
                            self.last_partial_text = partial_text
                            
                            # Добавляем частичный текст в буфер для анализа длинных фраз
                            self._add_to_buffer(partial_text, current_time, is_partial=True)
                            self._process_buffer()
                
                # Периодическая очистка буфера
                self._cleanup_buffer(current_time)
    
    def _add_to_buffer(self, text: str, timestamp: float, is_partial: bool = False):
        """Добавляет текст в буфер с временной меткой."""
        self.text_buffer.append({
            'text': text,
            'timestamp': timestamp,
            'is_partial': is_partial
        })
        self.last_activity_time = timestamp
    
    def _cleanup_buffer(self, current_time: float):
        """Удаляет старые записи из буфера."""
        cutoff_time = current_time - self.buffer_duration
        while self.text_buffer and self.text_buffer[0]['timestamp'] < cutoff_time:
            self.text_buffer.popleft()
    
    def _is_significant_change(self, new_text: str) -> bool:
        """Проверяет, существенно ли изменился частичный текст."""
        if not self.last_partial_text:
            return True
        
        # Если новый текст значительно длиннее или содержит новые слова
        if len(new_text) > len(self.last_partial_text) + 10:
            return True
        
        # Если появились новые слова в конце
        new_words = set(new_text.split())
        old_words = set(self.last_partial_text.split())
        return len(new_words - old_words) > 0
    
    def _process_buffer(self):
        """Обрабатывает накопленный в буфере текст."""
        if not self.text_buffer:
            return
        
        # Создаем объединенный текст из последних записей
        recent_texts = []
        current_time = time.time()
        
        # Берем тексты за последние 10 секунд для анализа контекста
        context_window = 10
        cutoff_time = current_time - context_window
        
        for entry in self.text_buffer:
            if entry['timestamp'] >= cutoff_time:
                # Исключаем частичные дубли полных результатов
                if not entry['is_partial'] or not self._is_duplicate_of_recent_full(entry['text']):
                    recent_texts.append(entry['text'])
        
        if recent_texts:
            # Объединяем тексты и обрабатываем
            combined_text = ' '.join(recent_texts)
            self._process_recognized_text(combined_text)
            
            # Также обрабатываем последний полный текст отдельно
            last_full_texts = [entry['text'] for entry in self.text_buffer 
                             if not entry['is_partial']]
            if last_full_texts:
                self._process_recognized_text(last_full_texts[-1])
    
    def _is_duplicate_of_recent_full(self, partial_text: str) -> bool:
        """Проверяет, не является ли частичный текст дублем недавнего полного результата."""
        for entry in reversed(list(self.text_buffer)):
            if not entry['is_partial']:
                if partial_text in entry['text'] or entry['text'] in partial_text:
                    return True
                break  # Проверяем только последний полный результат
        return False
    
    def _process_recognized_text(self, text: str):
        """Обрабатывает распознанный текст через callback-функцию."""
        if self.phrase_processor:
            try:
                self.phrase_processor(text)
            except Exception as e:
                self.logger.error(f"Ошибка при обработке фразы '{text}': {e}")
        else:
            self.logger.warning(f"Нет обработчика для фразы: {text}")
    
    def get_recent_text(self, duration: int = 15) -> str:
        """Возвращает недавно распознанный текст за указанное время."""
        current_time = time.time()
        cutoff_time = current_time - duration
        
        recent_texts = []
        for entry in self.text_buffer:
            if entry['timestamp'] >= cutoff_time and not entry['is_partial']:
                recent_texts.append(entry['text'])
        
        return ' '.join(recent_texts)
