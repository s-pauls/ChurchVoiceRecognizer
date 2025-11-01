from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from actions import (action_reader_only, action_altar_only,
                       action_altar_and_reader, action_altar_and_chorus, action_altar_and_chorus_reverb,
                       action_reader_remote, action_switch_off_all_mics)

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
    timeoutSeconds: Optional[int] = None  # Максимальное время ожидания перехода

def get_default_config() -> Dict[str, StateTransition]:
    """Возвращает конфигурацию блоков по умолчанию"""
    return {
        "START": StateTransition(
            # timeoutSeconds=5*60,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=[
                        "благословен бог", "веки веков",
                        "аминь",
                        "слава тебе боже", "слава тебе боже наш",
                        "царю небесный", "утешителю", "и очисти",
                        "христос воскресе",
                        "святый боже", "крепкий", "помилуй нас",
                    ],
                    next_state="3_ЧАС_НАЧАЛСЯ"
                )
            ],
        ),
        "3_ЧАС_НАЧАЛСЯ": StateTransition(
            timeoutSeconds=70,  # До первого "Отче наш" одна минута
            onBeginAction=action_reader_only,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=OTCHE_NASH,
                    next_state="3_ЧАС_ОТЧЕ_НАШ_1_НАЧАЛСЯ"
                )
            ],
        ),
        "3_ЧАС_ОТЧЕ_НАШ_1_НАЧАЛСЯ": StateTransition(
            timeoutSeconds=35,  # От начала стейта с учетом ожидания в 12 сек.
            onBeginDelaySeconds=12,
            onBeginAction=action_altar_and_reader,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["timeout"], # "аминь", "господи помилуй"
                    next_state="3_ЧАС_ОТЧЕ_НАШ_1_ЗАКОНЧИЛСЯ"
                )
            ],
        ),
        "3_ЧАС_ОТЧЕ_НАШ_1_ЗАКОНЧИЛСЯ": StateTransition(
            onBeginAction=action_reader_only,
            afterActionSleepSeconds=5 * 60,
            timeoutSeconds=9*60,  # 8 минут от ГП до второго ОН, на пасхальной службе вставка
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=OTCHE_NASH,
                    next_state="3_ЧАС_ОТЧЕ_НАШ_2_НАЧАЛСЯ"
                )
            ],
        ),
        "3_ЧАС_ОТЧЕ_НАШ_2_НАЧАЛСЯ": StateTransition(
            timeoutSeconds=35,  # От начала стейта с учетом ожидания в 12 сек.
            onBeginDelaySeconds=12,
            onBeginAction=action_altar_and_reader,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["timeout"],
                    next_state="3_ЧАС_ОТЧЕ_НАШ_2_ЗАКОНЧИЛСЯ"
                )
            ],
        ),
        "3_ЧАС_ОТЧЕ_НАШ_2_ЗАКОНЧИЛСЯ": StateTransition(
            timeoutSeconds=190,  # 10:15 закончился ОН 12:30 нужен переход + 50 сек если служба Пасхальная .
            onBeginAction=action_reader_only,
            afterActionSleepSeconds=1 * 60,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["херувим", "без сравнения", "серафим", "бога слова", "богородицу"],
                    next_state="3_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_НАЧАЛО"
                )
            ],
        ),
        "3_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_НАЧАЛО": StateTransition(
            timeoutSeconds=20,  # Возглас длиться 8 сек.
            onBeginAction=action_altar_and_reader,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["***"], # "аминь", "боже", "святый", "помилуй"
                    next_state="3_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_КОНЕЦ"
                )
            ],
        ),
        "3_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_КОНЕЦ": StateTransition(
            onBeginAction=action_reader_only,
            afterActionSleepSeconds=1 * 60,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["придите поклонимся", "придите поклониться", "самому христу"],
                    next_state="6_ЧАС_НАЧАЛСЯ"
                )
            ],
        ),
        "6_ЧАС_НАЧАЛСЯ": StateTransition(
            afterActionSleepSeconds=4 * 60,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=OTCHE_NASH,
                    next_state="6_ЧАС_ОТЧЕ_НАШ_НАЧАЛСЯ"
                )
            ],
        ),
        "6_ЧАС_ОТЧЕ_НАШ_НАЧАЛСЯ": StateTransition(
            timeoutSeconds=35,  # От начала стейта с учетом ожидания в 12 сек.
            onBeginDelaySeconds=12,
            onBeginAction=action_altar_and_reader,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["timeout"],
                    next_state="6_ЧАС_ОТЧЕ_НАШ_ЗАКОНЧИЛСЯ"
                )
            ],
        ),
        "6_ЧАС_ОТЧЕ_НАШ_ЗАКОНЧИЛСЯ": StateTransition(
            onBeginAction=action_reader_only,
            afterActionSleepSeconds=1 * 60,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["херувим", "без сравнения", "серафим", "бога слова", "богородицу"],
                    next_state="6_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_НАЧАЛО"
                )
            ],
        ),
        "6_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_НАЧАЛО": StateTransition(
            timeoutSeconds=20,  # Возглас длиться 8 сек.
            onBeginAction=action_altar_and_reader,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["***"], # Василия великого "аминь", "боже", "господа нашего", "иисуса христа", "прийми", "пригвозди"
                    next_state="6_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_КОНЕЦ"
                )
            ],
        ),
        "6_ЧАС_ЧЕСТНЕЙШУЮ_ХЕРУВИМ_КОНЕЦ": StateTransition(
            onBeginAction=action_reader_only,
            afterActionSleepSeconds=10,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["благословенно царство", "отца", "сына", "святого духа", "аминь"],
                    next_state="ЛИТУРГИЯ_ОГЛАШЕННЫХ_НАЧАЛО"
                )
            ],
        ),
        "ЛИТУРГИЯ_ОГЛАШЕННЫХ_НАЧАЛО": StateTransition( # до Сугубой 18 минут, до Херувимской 27 минут
            onBeginAction=action_altar_and_chorus,
            # timeoutSeconds=20 * 60, # Максимум 20 минут до Сугубой ектении
            afterActionSleepSeconds=45 *60,# 15 * 60,
            transitions=[

                StateTransitionCondition(
                    trigger_phrases=["молитвами святых", "отец наших"],
                    next_state="ЗАПРИЧАСТНОЕ_ЧТЕНИЕ",
                ),
                StateTransitionCondition(
                    trigger_phrases=[""],
                    next_state="МОЛИТВЫ_ПЕРЕД_ПРИЧАСТИЕМ",
                ),
                StateTransitionCondition(
                    trigger_phrases=["во имя отца и сына", "духа", "спаси господи всех", "причастников с принятием"],
                    next_state="ПРОПОВЕДЬ",
                ),

                '''
                StateTransitionCondition(
                    trigger_phrases=["eще молимся", "eщё молимся", "всего помышления нашего", "господи помилуй господи помилуй", "кирилл", "стефан"],
                    next_state="СУГУБАЯ_ЕКТЕНИЯ"
                ),
            
                '''
            ],
        ),
        '''
        "СУГУБАЯ_ЕКТЕНИЯ": StateTransition(
            onBeginAction=action_altar_and_chorus_reverb,
            # timeoutSeconds=10 * 60, # Максимум 10 минут до Херувимской
            # afterActionSleepSeconds=23*60, # до Херувимской 27 минут
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["мире всего мира", "храме", "под державою"],
                    next_state="ЛИТУРГИЯ_ВЕРНЫХ_ХЕРУВИМСКАЯ"
                )
            ],
        ),

        "ЛИТУРГИЯ_ВЕРНЫХ_ХЕРУВИМСКАЯ": StateTransition(
            onBeginAction=action_altar_and_chorus_reverb,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["исполним молитву", "нашу"],
                    next_state="ЕКТЕНИЯ_ПРОСИТЕЛЬНАЯ"
                )
            ],
        ),
        "ЕКТЕНИЯ_ПРОСИТЕЛЬНАЯ": StateTransition(
            onBeginAction=action_altar_and_chorus,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["станем", "возношение", "в мире"],
                    next_state="СВЯТОЕ_ВОЗНОШЕНИЕ",
                )
            ],
        ),
        "СВЯТОЕ_ВОЗНОШЕНИЕ": StateTransition(
            onBeginAction=action_altar_and_chorus_reverb,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["кирилла", "минского", "заславского", "архиепископа"], # После "Достойно есть"
                    next_state="И_ДАЖДЬ_НАМ_ЕДИНЕМИ_УСТЫ",
                )
            ],
        ),
        '''
        
        "И_ДАЖДЬ_НАМ_ЕДИНЕМИ_УСТЫ": StateTransition(
            onBeginAction=action_altar_and_chorus,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["молитвами святых", "отец наших"],
                    next_state="ЗАПРИЧАСТНОЕ_ЧТЕНИЕ",
                ),
                StateTransitionCondition(
                    trigger_phrases=[""],
                    next_state="МОЛИТВЫ_ПЕРЕД_ПРИЧАСТИЕМ",
                )
            ],
        ),

        "ЗАПРИЧАСТНОЕ_ЧТЕНИЕ": StateTransition(
            onBeginAction=action_reader_remote,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["cо страхом божиим", "и верою приступите"],
                    next_state="ПРИЧАСТИЕ",
                )
            ],
        ),
        "МОЛИТВЫ_ПЕРЕД_ПРИЧАСТИЕМ": StateTransition(
            onBeginAction=action_reader_only,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["cо страхом божиим", "и верою приступите"],
                    next_state="ПРИЧАСТИЕ",
                )
            ],
        ),
        "ПРИЧАСТИЕ": StateTransition(
            timeoutSeconds=60,
            onBeginAction=action_altar_and_chorus,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["спаси боже", "люди твоя", "благослови достояние"],
                    next_state="ПО_ПРИЧАЩЕНИИ",
                )
            ],
        ),
        "ПО_ПРИЧАЩЕНИИ": StateTransition(
            onBeginAction=action_altar_and_chorus,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=["во имя отца и сына", "духа", "спаси господи всех", "причастников с принятием"],
                    next_state="ПРОПОВЕДЬ",
                )
            ],
        ),
        "ПРОПОВЕДЬ":StateTransition(
            onBeginAction=action_altar_only,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=[""],
                    next_state="ангела-хранителя",
                )
            ],
        ),
        "STOP": StateTransition(
            onBeginAction=action_switch_off_all_mics,
            transitions=[
                StateTransitionCondition(
                    trigger_phrases=[],
                    next_state="",
                )
            ],
        ),
    }