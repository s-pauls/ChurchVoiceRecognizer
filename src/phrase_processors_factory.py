"""
Модуль с различными обработчиками фраз для разных типов церковных служб.
"""
from typing import List
from processors.liturgy_fsm import LiturgyFSM
from processors.vesper_processor import VesperProcessor
from processors.simple_keyword_processor import SimpleKeywordProcessor
from processors.base_processor import BaseProcessor


def create_base_processor(logger):
    """Создает процессор для литургии."""
    processor = BaseProcessor(logger)
    return processor.process_phrase

def create_liturgy_processor(logger):
    """Создает процессор для литургии."""
    fsm = LiturgyFSM(logger)
    return fsm.process_phrase


def create_vesper_processor(logger):
    """Создает процессор для вечерней службы."""
    processor = VesperProcessor(logger)
    return processor.process_phrase


def create_keyword_processor(logger, keywords: List[str]):
    """Создает простой процессор ключевых слов."""
    processor = SimpleKeywordProcessor(logger, keywords)
    return processor.process_phrase


# Предустановленные конфигурации
SERVICE_PROCESSORS = {
    "базовый": create_base_processor,
    "литургия": create_liturgy_processor,
    "вечерня": create_vesper_processor,
    "утреня": lambda logger: create_keyword_processor(
        logger, 
        ["аллилуйя", "слава в вышних", "хвалите господа"]
    ),
    "молебен": lambda logger: create_keyword_processor(
        logger,
        ["господи помилуй", "святый боже", "пресвятая богородице"]
    )
}