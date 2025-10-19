#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест для проверки логики добавления новых частей текста в буфер.
"""

import sys
import os
import time
from collections import deque

# Добавляем src в path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class MockLogger:
    def info(self, msg): print(f"INFO: {msg}")
    def warning(self, msg): print(f"WARNING: {msg}")
    def error(self, msg): print(f"ERROR: {msg}")

def test_get_new_text_part():
    """Тест метода _get_new_text_part."""
    
    # Создаем минимальный экземпляр VoiceRecognizer для тестирования
    class TestRecognizer:
        def __init__(self):
            self.text_buffer = deque()
            self.last_activity_time = time.time()
        
        def _get_new_text_part(self, text: str) -> str:
            """Определяет новую часть текста, которой еще нет в буфере."""
            if not text or not self.text_buffer:
                return text
            
            # Получаем все тексты из буфера в одну строку
            existing_texts = []
            for entry in self.text_buffer:
                existing_texts.append(entry['text'])
            
            combined_existing = ' '.join(existing_texts)
            
            # Разбиваем входящий и существующий тексты на слова
            new_words = text.split()
            existing_words = combined_existing.split()
            
            # Находим индекс, с которого начинаются новые слова
            new_words_start_index = 0
            
            # Проверяем различные варианты пересечения
            for i in range(len(new_words)):
                # Проверяем, есть ли подстрока new_words[i:] в конце existing_words
                remaining_new_words = new_words[i:]
                if len(remaining_new_words) > len(existing_words):
                    continue
                    
                # Проверяем совпадение с концом существующих слов
                if len(existing_words) >= len(remaining_new_words):
                    if existing_words[-len(remaining_new_words):] == remaining_new_words:
                        # Все оставшиеся слова уже есть в буфере
                        return ""
                        
                # Проверяем частичное совпадение
                match_found = False
                for j in range(min(len(remaining_new_words), len(existing_words))):
                    if existing_words[-(j+1):] == remaining_new_words[:j+1]:
                        new_words_start_index = i + j + 1
                        match_found = True
                        break
                
                if match_found:
                    break
                    
            # Возвращаем только новые слова
            if new_words_start_index < len(new_words):
                return ' '.join(new_words[new_words_start_index:])
            
            return ""
        
        def add_to_buffer_test(self, text: str):
            """Тестовый метод для добавления в буфер."""
            new_part = self._get_new_text_part(text)
            if new_part:
                self.text_buffer.append({
                    'text': new_part,
                    'timestamp': time.time(),
                    'is_partial': False
                })
                print(f"Добавлено в буфер: '{new_part}'")
            else:
                print(f"Ничего нового для добавления из: '{text}'")
            
            # Показываем текущее состояние буфера
            buffer_texts = [entry['text'] for entry in self.text_buffer]
            print(f"Текущий буфер: {buffer_texts}")
            print("---")

    # Создаем экземпляр для тестирования
    recognizer = TestRecognizer()
    
    print("=== Тест логики добавления новых частей текста ===\n")
    
    # Тест 1: Пустой буфер
    print("Тест 1: Пустой буфер")
    recognizer.add_to_buffer_test("привет мир")
    
    # Тест 2: Полное дублирование
    print("Тест 2: Полное дублирование")
    recognizer.add_to_buffer_test("привет мир")
    
    # Тест 3: Добавление нового слова
    print("Тест 3: Добавление нового слова")
    recognizer.add_to_buffer_test("привет мир как дела")
    
    # Тест 4: Новое предложение
    print("Тест 4: Новое предложение")
    recognizer.add_to_buffer_test("сегодня хорошая погода")
    
    # Тест 5: Частичное совпадение
    print("Тест 5: Частичное совпадение с концом")
    recognizer.add_to_buffer_test("хорошая погода завтра")
    
    # Тест 6: Полностью новый текст
    print("Тест 6: Полностью новый текст")
    recognizer.add_to_buffer_test("время идти домой")

if __name__ == "__main__":
    test_get_new_text_part()