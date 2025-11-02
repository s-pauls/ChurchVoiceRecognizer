import os
import subprocess
import winsound
from logger import setup_logger
from send_keys_to_obs_simple import OBSHotkeySimple

logger = setup_logger(name="actions", log_file="actions.log")

CTRL_SHIFT_X = "^(+(X))"
CTRL_SHIFT_A = "^(+(A))"
CTRL_SHIFT_P = "^(+(P))"
CTRL_SHIFT_D = "^(+(D))"
CTRL_SHIFT_B = "^(+(B))"
CTRL_SHIFT_H = "^(+(H))"
CTRL_SHIFT_T = "^(+(T))"

def action_altar_and_chorus():
    logger.info("✅ Действие Алтарь + Хор")
    manager = OBSHotkeySimple()
    manager.send_ctrl_shift_t()

def action_altar_and_chorus_reverb():
    logger.info("✅ Действие Алтарь + Хор (протяжно)")
    manager = OBSHotkeySimple()
    manager.send_ctrl_shift_p()

def action_altar_and_reader():
    logger.info("✅ Действие Алтарь + Чтец")
    manager = OBSHotkeySimple()
    manager.send_ctrl_shift_h()

def action_altar_only():
    logger.info("✅ Действие Алтарь")
    manager = OBSHotkeySimple()
    manager.send_ctrl_shift_a()

def action_reader_only():
    logger.info("✅ Действие Чтец")
    manager = OBSHotkeySimple()
    manager.send_ctrl_shift_b()

def action_reader_remote():
    logger.info("✅ Действие Чтец (петличка)")
    manager = OBSHotkeySimple()
    manager.send_ctrl_shift_d()

def action_switch_off_all_mics():
    logger.info("✅ Действие Выключить все микрофоны")
    manager = OBSHotkeySimple()
    manager.send_ctrl_shift_x()

def action_play_bam():
    """Воспроизводит файл bam.wav"""
    try:
        bam_file_path = os.path.abspath(os.path.join("media", "bam.wav"))
        
        if os.path.exists(bam_file_path):
            # Используем winsound для прямого воспроизведения WAV файла
            winsound.PlaySound(bam_file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            logger.info("✅ Действие Запуск файла bam.wav")
        else:
            logger.error(f"Файл {bam_file_path} не найден")
    except Exception as e:
        logger.error(f"Ошибка при воспроизведении bam.wav: {e}")

def send_keys_to_obs(hotkey: str):
    try:
        vbs_path = os.path.abspath("scripts\\sendKeysTo.vbs")
        obs_exe = "obs64.exe"

        # Формируем аргументы для передачи в VBS
        args = f'"{vbs_path}" "{obs_exe}" "{hotkey}"'
        subprocess.run(f'cscript {args}', shell=True)

    # self.logger.info("VBS-скрипт для OBS успешно запущен")
    except Exception as e:
        logger.error(f"Ошибка при запуске VBS: {e}")

def shutdown():
    try:
        vbs_path = os.path.abspath("scripts\\shutdown_script.vbs")
        # Формируем аргументы для передачи в VBS
        args = f'"{vbs_path}"'
        subprocess.run(f'cscript {args}', shell=True)
    except Exception as e:
        logger.error(f"Ошибка при запуске VBS: {e}")

def start_aimp():
    try:
        vbs_path = os.path.abspath("scripts\\start_aimp.vbs")
        # Формируем аргументы для передачи в VBS
        args = f'"{vbs_path}"'
        subprocess.run(f'cscript {args}', shell=True)
    except Exception as e:
        logger.error(f"Ошибка при запуске VBS: {e}")

def stop_aimp():
    try:
        vbs_path = os.path.abspath("scripts\\stop_aimp.vbs")
        # Формируем аргументы для передачи в VBS
        args = f'"{vbs_path}"'
        subprocess.run(f'cscript {args}', shell=True)
    except Exception as e:
        logger.error(f"Ошибка при запуске VBS: {e}")