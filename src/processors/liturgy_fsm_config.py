from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from src.actions import action_reader_only, action_altar_and_reader

OTCHE_NASH = ["отче наш", "имя твое", "царствие твое", "долги наши",
                "отче наш иже еси", "да святится имя", "да приидет царствие",
                "и остави нам долги"]

@dataclass
class StateTransitionCondition:
    trigger_phrases: List[str]  # Фразы, которые запускают переход
    next_state: str             # Указывает куда перейти

@dataclass
class StateTransition:
    """Описание перехода между состояниями"""
    transitions: List[StateTransitionCondition]  # Фразы, которые запускают переход
    onBeginDelaySeconds: Optional[int] = None # Задержка перед действием
    onBeginAction: Optional[Callable] = None
    afterActionSleepSeconds: Optional[int] = None  # Задержка после действия
    afterSleepAction: Optional[Callable] = None

def get_default_config() -> Dict[str, StateTransition]:
    """Возвращает конфигурацию блоков по умолчанию"""
    return {
        "START": StateTransition(
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=[
                        "благословен бог", "веки веков",
                        "аминь",
                        "слава тебе боже", "слава тебе боже наш",
                        "царю небесный", "утешителю", "и очисти", "крепкий", "помилуй нас",
                    ],
                    next_state="3_ЧАС_НАЧАЛСЯ"
            )],
        ),
        "3_ЧАС_НАЧАЛСЯ": StateTransition(
            onBeginAction=action_reader_only,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=OTCHE_NASH,
                    next_state="3_ЧАС_ОТЧЕ_НАШ_1_НАЧАЛСЯ"
                )],
        ),
        "3_ЧАС_ОТЧЕ_НАШ_1_НАЧАЛСЯ": StateTransition(
            onBeginDelaySeconds=12,
            onBeginAction=action_altar_and_reader,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["аминь", "господи помилуй"],
                    next_state="3_ЧАС_ОТЧЕ_НАШ_1_ЗАКОНЧИЛСЯ"
                )],

        ),
        "3_ЧАС_ОТЧЕ_НАШ_1_ЗАКОНЧИЛСЯ": StateTransition(
            onBeginAction=action_reader_only,
            afterActionSleepSeconds=5 * 60,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=OTCHE_NASH,
                    next_state="3_ЧАС_ОТЧЕ_НАШ_2_НАЧАЛСЯ"
                )],
        ),
        "3_ЧАС_ОТЧЕ_НАШ_2_НАЧАЛСЯ": StateTransition(
            onBeginDelaySeconds=12,
            onBeginAction=action_altar_and_reader,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["аминь", "господи помилуй"],
                    next_state="3_ЧАС_ОТЧЕ_НАШ_2_ЗАКОНЧИЛСЯ"
                )],
        ),
        "3_ЧАС_ОТЧЕ_НАШ_2_ЗАКОНЧИЛСЯ": StateTransition(
            onBeginAction=action_reader_only,
            afterActionSleepSeconds=1 * 60,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["херувим", "без сравнения", "серафим", "бога слова", "богородицу"],
                    next_state="3_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_НАЧАЛО"
                )],
        ),
        "3_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_НАЧАЛО": StateTransition(
            onBeginAction=action_altar_and_reader,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["аминь", "боже", "святый", "помилуй"],
                    next_state="3_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_КОНЕЦ"
                )],
        ),
        "3_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_КОНЕЦ": StateTransition(
            onBeginAction=action_reader_only,
            afterActionSleepSeconds=1 * 60,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["придите поклонимся", "придите поклониться", "самому христу"],
                    next_state="6_ЧАС_НАЧАЛСЯ"
                )],
        ),
        "6_ЧАС_НАЧАЛСЯ": StateTransition(
            afterActionSleepSeconds=4 * 60,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=OTCHE_NASH,
                    next_state="6_ЧАС_ОТЧЕ_НАШ_НАЧАЛСЯ"
                )],
        ),
        "6_ЧАС_ОТЧЕ_НАШ_НАЧАЛСЯ": StateTransition(
            onBeginDelaySeconds=12,
            onBeginAction=action_altar_and_reader,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["аминь", "господи помилуй"],
                    next_state="6_ЧАС_ОТЧЕ_НАШ_ЗАКОНЧИЛСЯ"
                )],
        ),
        "6_ЧАС_ОТЧЕ_НАШ_ЗАКОНЧИЛСЯ": StateTransition(
            onBeginAction=action_reader_only,
            afterActionSleepSeconds=1 * 60,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["придите поклонимся", "придите поклониться", "самому христу"],
                    next_state="6_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_НАЧАЛО"
                )],
        ),
        "6_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_НАЧАЛО": StateTransition(
            onBeginAction=action_altar_and_reader,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["аминь", "боже", "святый", "помилуй"],
                    next_state="6_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_КОНЕЦ"
                )],
        ),
        "6_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_КОНЕЦ": StateTransition(
            onBeginAction=action_reader_only,
            afterActionSleepSeconds=10,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["аминь", "боже", "господа нашего", "иисуса христа", "прийми", "пригвозди"],
                    next_state=""
                )],
        ),
    }