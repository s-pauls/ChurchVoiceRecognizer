import time
from typing import Dict, List, Optional
from src.processors.liturgy_fsm_config import get_default_config, StateTransition


class LiturgyFSM:
    def __init__(self, logger, states_config: Optional[Dict[str, StateTransition]] = None):
        self.current_state_name: str = "START"
        self.current_state : Optional[StateTransition] = None
        self.state_start_time = None
        self.logger = logger
        
        # Инициализируем конфигурацию блоков
        self.states_config = states_config if states_config else get_default_config()

    def wait_timeout(self) -> bool:
        """Проверяет истечение таймаута текущего блока"""
        if not self.state_start_time or not self.current_state:
            return False
            
        state_config = self.states_config.get(self.current_state_name)
        if not state_config:
            return False

        elapsed_time = time.time() - self.state_start_time
        if state_config.onBeginDelaySeconds and elapsed_time < state_config.onBeginDelaySeconds:
            self.logger.info("⏳ Ожидание таймаута блока "f"'{self.current_state_name}' "
                             f"({int(elapsed_time)}/{state_config.onBeginDelaySeconds}с)")
            return True
        return False

    def process_phrase(self, phrase: str) -> bool:
        phrase_lower = phrase.lower()
        
        # Проверяем таймаут
        if self.wait_timeout():
            return False
            
        # Ищем подходящий переход для текущего состояния
        transition, next_state = self._find_transition(phrase_lower)
        if transition:
            self._execute_transition(transition, next_state)
            return True
        else:
            pass
            # Дополнительно проверяем, есть ли триггеры в тексте для любого состояния
            # Это поможет восстановиться, если мы пропустили переход
            # self._check_recovery_transitions(phrase_lower)

        return False

    def _find_transition(self, phrase: str) -> Optional[StateTransition, str]:
        state_transition = self.states_config.get(self.current_state_name)
        if state_transition:
            for transition in state_transition.transitions:
                if self._phrase_matches_triggers(phrase, transition.trigger_phrases):
                    return state_transition, transition.next_state
        return None, None
    
    @staticmethod
    def _phrase_matches_triggers(phrase: str, triggers: List[str]) -> bool:
        return any(trigger.lower() in phrase for trigger in triggers)

    def _execute_transition(self, transition: StateTransition, next_state: str):
        old_state = self.current_state_name
        self.current_state_name = next_state

        state_config = self.states_config.get(self.current_state_name)
        if state_config:
            self.current_state = state_config

        self.logger.info(f"▶️ Переход: {old_state} → {self.current_state_name}")

        # Выполняем действие, если оно задано
        if transition.onBeginAction:
            self.logger.info(f"⚙️ Выполнение действия состояния '{self.current_state_name}'")
            transition.onBeginAction()

        if transition.afterSleepAction:
            self.logger.info(f"⚙️ Выполнение действия состояния '{self.current_state_name}'")
            transition.afterSleepAction()

        self.start_state_timer(self.current_state_name, state_config)
    
    def start_state_timer(self, state_name: str, state: StateTransition):
        if state and state.onBeginDelaySeconds and state.onBeginDelaySeconds > 0:
            self.state_start_time = time.time()
            self.logger.info(f"🕐 Запущен таймер для состояния '{state_name}' ({state.onBeginDelaySeconds}с)")

    def reset(self):
        """Сбрасывает FSM в начальное состояние"""
        self.current_state_name = "START"
        self.current_state = None
        self.state_start_time = None
        print("🔄 FSM сброшен в начальное состояние")
