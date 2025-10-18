import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from src.actions import action_altar_and_reader, action_reader_only

@dataclass
class StateTransition:
    """Описание перехода между состояниями"""
    trigger_phrases: List[str]  # Фразы, которые запускают переход
    next_state: str
    timeout: Optional[int] = None # Таймаут блока в секундах
    action: Optional[Callable] = None

class LiturgyFSM:
    def __init__(self, logger, states_config: Optional[Dict[str, StateTransition]] = None):
        self.current_state_name: str = "START"
        self.current_state : Optional[StateTransition] = None
        self.state_start_time = None
        self.logger = logger
        
        # Инициализируем конфигурацию блоков
        self.states_config = states_config if states_config else self._get_default_config()

    def check_timeout(self):
        """Проверяет истечение таймаута текущего блока"""
        if not self.state_start_time or not self.current_state:
            return False
            
        state_config = self.states_config.get(self.current_state_name)
        if not state_config:
            return False

        elapsed_time = time.time() - self.state_start_time
        if elapsed_time > state_config.timeout:
            print(f"⏱️ Таймер истёк для блока '{self.current_state_name}' ({elapsed_time:.1f}с)")
            self._handle_timeout()
            return True
        return False
    
    def _handle_timeout(self):
        if self.current_state.next_state:
            self.current_state_name = self.current_state.next_state
            print(f"Переход в состояние: {self.current_state.next_state}")

        self.state_start_time = None
        self.current_state = None

    def process_phrase(self, phrase: str) -> bool:
        phrase_lower = phrase.lower()
        
        # Проверяем таймаут
        if self.check_timeout():
            return False
            
        # Ищем подходящий переход для текущего состояния
        transition = self._find_transition(phrase_lower)
        if transition:
            self._execute_transition(transition)
            return True
        else:
            pass
            # Дополнительно проверяем, есть ли триггеры в тексте для любого состояния
            # Это поможет восстановиться, если мы пропустили переход
            # self._check_recovery_transitions(phrase_lower)

        return False

    def _find_transition(self, phrase: str) -> Optional[StateTransition]:
        state_transition = self.states_config.get(self.current_state_name)
        if state_transition and self._phrase_matches_triggers(phrase, state_transition.trigger_phrases):
            return state_transition
        return None
    
    def _phrase_matches_triggers(self, phrase: str, triggers: List[str]) -> bool:
        return any(trigger.lower() in phrase for trigger in triggers)
    
    def _check_recovery_transitions(self, phrase: str):
        """Проверяет возможность восстановления состояния по ключевым фразам."""
        # Ищем среди всех состояний те, чьи триггеры присутствуют в фразе
        for state_name, state_transition in self.states_config.items():
            if state_name != self.current_state_name:  # Не текущее состояние
                if self._phrase_matches_triggers(phrase, state_transition.trigger_phrases):
                    self.logger.info(f"Обнаружен переход восстановления: {self.current_state_name} → {state_name}")
                    self._execute_transition_to_state(state_name, state_transition)
                    break
    
    def _execute_transition_to_state(self, target_state: str, transition: StateTransition):
        """Выполняет переход в конкретное состояние."""
        old_state = self.current_state_name
        self.current_state_name = target_state
        
        state_config = self.states_config.get(target_state)
        if state_config:
            self.current_state = state_config
        
        self.start_state_timer(target_state, transition)
        
        # Выполняем действие, если оно задано
        if transition.action:
            transition.action()
        
        print(f"🔄 Восстановление состояния: {old_state} → {target_state}")
    
    def _execute_transition(self, transition: StateTransition):
        old_state = self.current_state_name
        self.current_state_name = transition.next_state

        state_config = self.states_config.get(self.current_state_name)
        if state_config:
            self.current_state = state_config

        self.start_state_timer(self.current_state_name, state_config)

        # Выполняем действие, если оно задано
        if transition.action:
            transition.action()

        print(f"▶️ Переход: {old_state} → {self.current_state_name}")
    
    def start_state_timer(self, state_name: str, state: StateTransition):
        if state and state.timeout and state.timeout > 0:
            self.state_start_time = time.time()
            print(f"🕐 Запущен таймер для блока '{state_name}' ({state.timeout}с)")

    def reset(self):
        """Сбрасывает FSM в начальное состояние"""
        self.current_state_name = "START"
        self.current_state = None
        self.state_start_time = None
        print("🔄 FSM сброшен в начальное состояние")

    def _get_default_config(self) -> Dict[str, StateTransition]:
        """Возвращает конфигурацию блоков по умолчанию"""
        return {
            "START": StateTransition(
                trigger_phrases=[
                    "слава тебе боже наш", "царю небесный", "приди", 
                    "и очисти", "крепкий", "помилуй нас", "слава тебе боже",
                    "царю небесный утешителю"
                ],
                next_state="THIRD_HOUR_STARTED"
            ),
            "THIRD_HOUR_STARTED": StateTransition(
                trigger_phrases=[
                    "отче наш", "имя твое", "царствие твое", "долги наши",
                    "отче наш иже еси", "да святится имя", "да приидет царствие",
                    "и остави нам долги"
                ],
                next_state="THIRD_HOUR_OTCHE_1",
                action=action_altar_and_reader,
            ),
            "THIRD_HOUR_OTCHE_1": StateTransition(
                trigger_phrases=["господи помилуй"],
                next_state="THIRD_HOUR_WAIT_2",
                action=action_reader_only
            ),
            "THIRD_HOUR_WAIT_2": StateTransition(
                trigger_phrases=[
                    "отче наш", "имя твое", "царствие твое", "долги наши",
                    "отче наш иже еси", "да святится имя", "да приидет царствие",
                    "и остави нам долги"
                ],
                next_state="THIRD_HOUR_OTCHE_2",
                action=action_altar_and_reader,
            ),
            "THIRD_HOUR_OTCHE_2": StateTransition(
                trigger_phrases=["господи помилуй"],
                next_state="THIRD_HOUR_END",
                action=action_reader_only
            ),
            "THIRD_HOUR_END": StateTransition(
                trigger_phrases=["слава тебе боже наш", "царю небесный", "приди", "и очисти", "крепкий", "помилуй нас"],
                next_state="SIXTH_HOUR_STARTED"
            ),
            "SIXTH_HOUR_STARTED": StateTransition(
                trigger_phrases=[
                    "отче наш", "имя твое", "царствие твое", "долги наши",
                    "отче наш иже еси", "да святится имя", "да приидет царствие",
                    "и остави нам долги"
                ],
                next_state="SIXTH_HOUR_OTCHE",
                action=action_altar_and_reader
            ),
            "SIXTH_HOUR_OTCHE": StateTransition(
                trigger_phrases=["господи помилуй"],
                next_state="SIXTH_HOUR_END",
                action=action_reader_only
            )
        }