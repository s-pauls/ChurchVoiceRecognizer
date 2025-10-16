import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable

@dataclass
class StateTransition:
    """Описание перехода между состояниями"""
    trigger_phrases: List[str]  # Фразы, которые запускают переход
    next_state: str
    action: Optional[Callable] = None
    increment_counter: bool = False

@dataclass
class BlockConfig:
    """Конфигурация блока литургии"""
    name: str
    timeout: int  # Таймаут блока в секундах
    states: Dict[str, StateTransition]
    counter_limit: Optional[int] = None  # Лимит счетчика для блока

class LiturgyFSM:
    def __init__(self, logger, blocks_config: Optional[Dict[str, BlockConfig]] = None):
        self.state = "START"
        self.current_block = None
        self.block_counter = 0
        self.block_start_time = None
        self.logger = logger
        
        # Инициализируем конфигурацию блоков
        self.blocks_config = blocks_config if blocks_config else self._get_default_config()

    def action_1(self):
        print("✅ Действие 1: Обработка 'Отче наш' + 'имя Твое'")

    def action_2(self):
        print("✅ Действие 2: Обработка 'Господи помилуй' после молитвы")

    def start_block_timer(self, block_name: str):
        """Запускает таймер для указанного блока"""
        self.current_block = block_name
        self.block_start_time = time.time()
        self.block_counter = 0
        block_config = self.blocks_config.get(block_name)
        if block_config:
            print(f"🕐 Запущен таймер для блока '{block_config.name}' ({block_config.timeout}с)")

    def check_timeout(self):
        """Проверяет истечение таймаута текущего блока"""
        if not self.block_start_time or not self.current_block:
            return False
            
        block_config = self.blocks_config.get(self.current_block)
        if not block_config:
            return False
            
        elapsed_time = time.time() - self.block_start_time
        if elapsed_time > block_config.timeout:
            print(f"⏱️ Таймер истёк для блока '{block_config.name}' ({elapsed_time:.1f}с)")
            self._handle_timeout()
            return True
        return False
    
    def _handle_timeout(self):
        """Обрабатывает истечение таймаута блока"""
        if self.current_block == "THIRD_HOUR":
            self.state = "THIRD_HOUR_END"
            print("Переход в состояние: THIRD_HOUR_END")
        elif self.current_block == "SIXTH_HOUR":
            self.state = "SIXTH_HOUR_END"
            print("Переход в состояние: SIXTH_HOUR_END")
        
        self.block_start_time = None
        self.current_block = None

    def process_phrase(self, phrase: str):
        """Обрабатывает распознанную фразу и выполняет переходы состояний"""
        phrase = phrase.lower()
        
        # Проверяем таймаут
        if self.check_timeout():
            return
            
        # Ищем подходящий переход для текущего состояния
        transition = self._find_transition(phrase)
        if transition:
            self._execute_transition(transition)
    
    def _find_transition(self, phrase: str) -> Optional[StateTransition]:
        """Находит подходящий переход для текущего состояния"""
        # Ищем во всех блоках
        for block_name, block_config in self.blocks_config.items():
            state_transition = block_config.states.get(self.state)
            if state_transition and self._phrase_matches_triggers(phrase, state_transition.trigger_phrases):
                return state_transition
        return None
    
    def _phrase_matches_triggers(self, phrase: str, triggers: List[str]) -> bool:
        """Проверяет, содержит ли фраза все необходимые триггеры"""
        return all(trigger.lower() in phrase for trigger in triggers)
    
    def _execute_transition(self, transition: StateTransition):
        """Выполняет переход состояния"""
        old_state = self.state
        self.state = transition.next_state
        
        # Выполняем действие, если оно задано
        if transition.action:
            transition.action()
            
        # Увеличиваем счетчик, если требуется
        if transition.increment_counter:
            self.block_counter += 1
            
        # Обрабатываем специальные состояния
        self._handle_special_states(old_state, transition.next_state)
        
        print(f"▶️ Переход: {old_state} → {self.state}")
    
    def _handle_special_states(self, old_state: str, new_state: str):
        """Обрабатывает специальные логики для определенных состояний"""
        # Запуск таймера при начале блоков
        if new_state == "THIRD_HOUR_STARTED":
            self.start_block_timer("THIRD_HOUR")
        elif new_state == "SIXTH_HOUR_STARTED":
            self.start_block_timer("SIXTH_HOUR")
            
        # Завершение блоков
        if new_state.endswith("_END"):
            self.block_start_time = None
            self.current_block = None

    def reset(self):
        """Сбрасывает FSM в начальное состояние"""
        self.state = "START"
        self.current_block = None
        self.block_counter = 0
        self.block_start_time = None
        print("🔄 FSM сброшен в начальное состояние")
        
    def get_current_status(self) -> Dict[str, any]:
        """Возвращает текущий статус FSM"""
        status = {
            "state": self.state,
            "current_block": self.current_block,
            "block_counter": self.block_counter,
            "block_start_time": self.block_start_time,
            "is_active": self.block_start_time is not None
        }
        
        if self.current_block and self.block_start_time:
            block_config = self.blocks_config.get(self.current_block)
            if block_config:
                elapsed = time.time() - self.block_start_time
                status["elapsed_time"] = elapsed
                status["remaining_time"] = max(0, block_config.timeout - elapsed)
                status["block_name"] = block_config.name
        
        return status
    
    def get_available_blocks(self) -> List[str]:
        """Возвращает список доступных блоков"""
        return list(self.blocks_config.keys())
    
    def update_block_timeout(self, block_name: str, new_timeout: int):
        """Обновляет таймаут для указанного блока"""
        if block_name in self.blocks_config:
            self.blocks_config[block_name].timeout = new_timeout
            print(f"📝 Обновлен timeout для блока '{block_name}': {new_timeout}с")

    def _get_default_config(self) -> Dict[str, BlockConfig]:
        """Возвращает конфигурацию блоков по умолчанию"""
        return {
            "THIRD_HOUR": BlockConfig(
                name="Третий час",
                timeout=600,  # 10 минут
                states={
                    "START": StateTransition(
                        trigger_phrases=["царю небесный"],
                        next_state="THIRD_HOUR_STARTED"
                    ),
                    "THIRD_HOUR_STARTED": StateTransition(
                        trigger_phrases=["отче наш", "имя твое"],
                        next_state="THIRD_HOUR_OTCHE_1",
                        action=self.action_1,
                        increment_counter=True
                    ),
                    "THIRD_HOUR_OTCHE_1": StateTransition(
                        trigger_phrases=["господи помилуй"],
                        next_state="THIRD_HOUR_WAIT_2",
                        action=self.action_2
                    ),
                    "THIRD_HOUR_WAIT_2": StateTransition(
                        trigger_phrases=["отче наш", "имя твое"],
                        next_state="THIRD_HOUR_OTCHE_2",
                        action=self.action_1,
                        increment_counter=True
                    ),
                    "THIRD_HOUR_OTCHE_2": StateTransition(
                        trigger_phrases=["господи помилуй"],
                        next_state="THIRD_HOUR_END",
                        action=self.action_2
                    )
                },
                counter_limit=2
            ),
            "SIXTH_HOUR": BlockConfig(
                name="Шестой час",
                timeout=480,  # 8 минут
                states={
                    "THIRD_HOUR_END": StateTransition(
                        trigger_phrases=["царю небесный"],
                        next_state="SIXTH_HOUR_STARTED"
                    ),
                    "SIXTH_HOUR_STARTED": StateTransition(
                        trigger_phrases=["отче наш", "имя твое"],
                        next_state="SIXTH_HOUR_OTCHE",
                        action=self.action_1
                    ),
                    "SIXTH_HOUR_OTCHE": StateTransition(
                        trigger_phrases=["господи помилуй"],
                        next_state="SIXTH_HOUR_END",
                        action=self.action_2
                    )
                }
            )
        }


if __name__ == "__main__":
    # Пример кастомной конфигурации с разными timeout'ами
    custom_config = {
        "THIRD_HOUR": BlockConfig(
            name="Третий час (быстрый)",
            timeout=30,  # Короткий timeout для тестирования
            states={
                "START": StateTransition(
                    trigger_phrases=["царю небесный"],
                    next_state="THIRD_HOUR_STARTED"
                ),
                "THIRD_HOUR_STARTED": StateTransition(
                    trigger_phrases=["отче наш", "имя твое"],
                    next_state="THIRD_HOUR_OTCHE_1",
                    action=lambda: print("✅ Действие 1: Обработка 'Отче наш' + 'имя Твое'"),
                    increment_counter=True
                ),
                "THIRD_HOUR_OTCHE_1": StateTransition(
                    trigger_phrases=["господи помилуй"],
                    next_state="THIRD_HOUR_WAIT_2",
                    action=lambda: print("✅ Действие 2: Обработка 'Господи помилуй' после молитвы")
                ),
                "THIRD_HOUR_WAIT_2": StateTransition(
                    trigger_phrases=["отче наш", "имя твое"],
                    next_state="THIRD_HOUR_OTCHE_2",
                    action=lambda: print("✅ Действие 1: Обработка 'Отче наш' + 'имя Твое'"),
                    increment_counter=True
                ),
                "THIRD_HOUR_OTCHE_2": StateTransition(
                    trigger_phrases=["господи помилуй"],
                    next_state="THIRD_HOUR_END",
                    action=lambda: print("✅ Действие 2: Обработка 'Господи помилуй' после молитвы")
                )
            },
            counter_limit=2
        ),
        "SIXTH_HOUR": BlockConfig(
            name="Шестой час (короткий)",
            timeout=20,  # Еще короче
            states={
                "THIRD_HOUR_END": StateTransition(
                    trigger_phrases=["царю небесный"],
                    next_state="SIXTH_HOUR_STARTED"
                ),
                "SIXTH_HOUR_STARTED": StateTransition(
                    trigger_phrases=["отче наш", "имя твое"],
                    next_state="SIXTH_HOUR_OTCHE",
                    action=lambda: print("✅ Действие 1: Обработка 'Отче наш' + 'имя Твое'")
                ),
                "SIXTH_HOUR_OTCHE": StateTransition(
                    trigger_phrases=["господи помилуй"],
                    next_state="SIXTH_HOUR_END",
                    action=lambda: print("✅ Действие 2: Обработка 'Господи помилуй' после молитвы")
                )
            }
        )
    }

    # Создаем FSM с кастомной конфигурацией
    fsm = LiturgyFSM(None, custom_config)
    
    print("🚀 Тестирование реструктурированного LiturgyFSM")
    print(f"📋 Доступные блоки: {fsm.get_available_blocks()}")
    
    # Симуляция распознанных фраз с задержками
    phrases = [
        ("Царю небесный", 0),
        ("Святый Боже", 1),
        ("Святый Крепкий", 1),
        ("Отче наш, да святится имя Твое", 2),
        ("Господи помилуй", 1),
        ("Отче наш, да святится имя Твое", 2),
        ("Господи помилуй", 1),
        ("Царю небесный", 3),
        ("Святый Боже", 1),
        ("Отче наш, да святится имя Твое", 2),
        ("Господи помилуй", 1)
    ]

    for i, (phrase, delay) in enumerate(phrases):
        time.sleep(delay)
        print(f"\n--- Фраза {i+1}: '{phrase}' ---")
        fsm.process_phrase(phrase)
        
        # Показываем статус
        status = fsm.get_current_status()
        print(f"📊 Состояние: {status['state']}")
        if status['current_block']:
            print(f"🕐 Блок: {status.get('block_name', status['current_block'])}")
            print(f"⏱️ Остается времени: {status.get('remaining_time', 0):.1f}с")
    
    print("\n🏁 Тестирование завершено")