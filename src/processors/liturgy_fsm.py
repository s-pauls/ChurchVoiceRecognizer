import time
from typing import Dict, List, Optional
from enum import Enum
from processors.liturgy_fsm_config import get_default_config, StateTransition


class StateExecutionPhase(Enum):
    """Фазы выполнения состояния"""
    READY = "ready"  # Готов к обработке фраз
    ON_BEGIN_DELAY = "on_begin_delay"  # Ожидание onBeginDelaySeconds
    ON_BEGIN_ACTION = "on_begin_action"  # Выполнение onBeginAction
    AFTER_ACTION_SLEEP = "after_action_sleep"  # Ожидание sleepTimeout
    AFTER_SLEEP_ACTION = "after_sleep_action"  # Выполнение afterSleepAction


class LiturgyFSM:
    def __init__(self, logger, states_config: Optional[Dict[str, StateTransition]] = None):
        self.current_state_name: str = "START"
        self.current_state : Optional[StateTransition] = None
        self.state_start_time = time.time()  # Запоминаем время перехода в состояние
        self.logger = logger
        
        # Фаза выполнения текущего состояния
        self.execution_phase = StateExecutionPhase.READY
        self.phase_start_time = None
        
        # Инициализируем конфигурацию блоков
        self.states_config = states_config if states_config else get_default_config()

    def process_phrase(self, phrase: str) -> bool:
        phrase_lower = phrase.lower()
        
        # Проверяем timeout состояния
        if self._check_state_timeout():
            return False  # Произошел timeout переход
        
        # Проверяем, выполняется ли состояние (задержки/действия)
        if self._execute_state_phases_if_not_busy():
            return False
            
        # Ищем подходящий переход для текущего состояния
        transition, next_state, matched_trigger = self._find_transition(phrase_lower)
        if transition:
            self._execute_transition(transition, next_state, matched_trigger)
            return True

        return False

    def _execute_state_phases_if_not_busy(self) -> bool:
        """Проверяет, выполняется ли состояние (задержки или действия)"""
        if self.execution_phase == StateExecutionPhase.READY:
            return False
            
        state_config = self.states_config.get(self.current_state_name)
        if not state_config or not self.phase_start_time:
            return False

        current_time = time.time()
        elapsed_time = current_time - self.phase_start_time

        # Проверяем текущую фазу
        if self.execution_phase == StateExecutionPhase.ON_BEGIN_DELAY:
            if state_config.onBeginDelaySeconds and elapsed_time < state_config.onBeginDelaySeconds:
                # self.logger.info(f"⏳ onBeginDelay для '{self.current_state_name}' "
                #               f"({int(elapsed_time)}/{state_config.onBeginDelaySeconds}с)")
                return True
            else:
                # Переходим к выполнению onBeginAction
                self._execute_on_begin_action()
                return True
                
        elif self.execution_phase == StateExecutionPhase.AFTER_ACTION_SLEEP:
            if state_config.afterActionSleepSeconds and elapsed_time < state_config.afterActionSleepSeconds:
                # if int(elapsed_time)==0 or int(elapsed_time)==state_config.sleepTimeout:
                #    self.logger.info(f"⏳ Ожидание после действия для '{self.current_state_name}' "
                #               f"({state_config.sleepTimeout}с)")
                return True
            else:
                # Переходим к выполнению afterSleepAction
                self._execute_after_sleep_action()
                return True
                
        return False

    def _check_state_timeout(self) -> bool:
        """Проверяет, не истек ли timeout для текущего состояния"""
        state_config = self.states_config.get(self.current_state_name)
        if not state_config or not state_config.timeoutSeconds or not self.state_start_time:
            return False
            
        current_time = time.time()
        elapsed_time = current_time - self.state_start_time

        if elapsed_time >= state_config.timeoutSeconds:
            self.logger.info(f"⏰ Timeout для состояния '{self.current_state_name}' "
                           f"({int(elapsed_time)}/{state_config.timeoutSeconds}с)")
            
            # Ищем первый доступный переход для автоматического перехода
            if state_config.transitions:
                first_transition = state_config.transitions[0]
                if first_transition.next_state:
                    self.logger.info(f"🔄 Автоматический переход по timeout: {self.current_state_name} → {first_transition.next_state}")
                    self._execute_transition(state_config, first_transition.next_state, "timeout")
                    return True
            
        return False

    def _execute_on_begin_action(self):
        """Выполняет onBeginAction и переходит к следующей фазе"""
        state_config = self.states_config.get(self.current_state_name)
        if not state_config:
            self._set_phase(StateExecutionPhase.READY)
            return
            
        self.execution_phase = StateExecutionPhase.ON_BEGIN_ACTION
        
        if state_config.onBeginAction:
            self.logger.info(f"⚙️ Выполнение onBeginAction для '{self.current_state_name}'")
            state_config.onBeginAction()
        
        # Переходим к sleepTimeout или завершаем
        if state_config.afterActionSleepSeconds and state_config.afterActionSleepSeconds > 0:
            self.logger.info(
                f"🕐 Запущен afterActionSleep для '{self.current_state_name}' ({state_config.afterActionSleepSeconds}с)")
            self._set_phase(StateExecutionPhase.AFTER_ACTION_SLEEP)
        else:
            self._execute_after_sleep_action()

    def _execute_after_sleep_action(self):
        """Выполняет afterSleepAction и завершает выполнение состояния"""
        state_config = self.states_config.get(self.current_state_name)
        if not state_config:
            self._set_phase(StateExecutionPhase.READY)
            return
            
        self.execution_phase = StateExecutionPhase.AFTER_SLEEP_ACTION
        
        if state_config.afterSleepAction:
            self.logger.info(f"⚙️ Выполнение afterSleepAction для '{self.current_state_name}'")
            state_config.afterSleepAction()
        
        # Завершаем выполнение состояния
        self._set_phase(StateExecutionPhase.READY)

    def _set_phase(self, phase: StateExecutionPhase):
        """Устанавливает новую фазу выполнения"""
        self.execution_phase = phase
        self.phase_start_time = time.time() if phase != StateExecutionPhase.READY else None


    def _find_transition(self, phrase: str) -> tuple[Optional[StateTransition], Optional[str], Optional[str]]:
        state_transition = self.states_config.get(self.current_state_name)
        if state_transition:
            for transition in state_transition.transitions:
                found, matched_trigger = self._phrase_matches_triggers(phrase, transition.trigger_phrases)
                if found:
                    return state_transition, transition.next_state, matched_trigger
        return None, None, None
    
    @staticmethod
    def _phrase_matches_triggers(phrase: str, triggers: List[str]) -> tuple[bool, Optional[str]]:
        for trigger in triggers:
            if trigger.lower() in phrase:
                return True, trigger
        return False, None

    def _execute_transition(self, transition: StateTransition, next_state: str, trigger: str):
        old_state = self.current_state_name
        self.current_state_name = next_state
        self.state_start_time = time.time()  # Запоминаем время перехода в новое состояние

        state_config = self.states_config.get(self.current_state_name)
        if state_config:
            self.current_state = state_config

        self.logger.info(f"▶️ Переход: {old_state} → {self.current_state_name} по фразе: '{trigger}'")

        # Запускаем последовательность выполнения нового состояния
        self._start_state_execution()

    def _start_state_execution(self):
        """Запускает последовательность выполнения состояния"""
        state_config = self.states_config.get(self.current_state_name)
        if not state_config:
            self._set_phase(StateExecutionPhase.READY)
            return

        # Проверяем, есть ли onBeginDelaySeconds
        if state_config.onBeginDelaySeconds and state_config.onBeginDelaySeconds > 0:
            self.logger.info(f"🕐 Запущен onBeginDelay для '{self.current_state_name}' ({state_config.onBeginDelaySeconds}с)")
            self._set_phase(StateExecutionPhase.ON_BEGIN_DELAY)
        else:
            # Если задержки нет, сразу выполняем onBeginAction
            self._execute_on_begin_action()

    def reset(self):
        """Сбрасывает FSM в начальное состояние"""
        self.current_state_name = "START"
        self.current_state = None
        self.state_start_time = time.time()  # Запоминаем время сброса
        self.execution_phase = StateExecutionPhase.READY
        self.phase_start_time = None
        print("🔄 FSM сброшен в начальное состояние")
