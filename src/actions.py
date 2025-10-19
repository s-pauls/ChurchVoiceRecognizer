import os
import subprocess
from logger import setup_logger

logger = setup_logger(name="actions", log_file="actions.log")


def action_altar_and_reader():
    logger.info("✅ Действие Алтарь + Чтец")

def action_reader_only():
    logger.info("✅ Действие Только чтец")

def action_switch_off_all_mics():
    logger.info("✅ Действие Выключить все микрофоны")

def send_keys_to_obs(hotkey: str):
    try:
        vbs_path = os.path.abspath("sendKeysTo.vbs")
        obs_exe = "obs64.exe"

        # Формируем аргументы для передачи в VBS
        args = f'"{vbs_path}" "{obs_exe}" "{hotkey}"'
        subprocess.run(f'cscript {args}', shell=True)

    # self.logger.info("VBS-скрипт для OBS успешно запущен")
    except Exception as e:
        logger.error(f"Ошибка при запуске VBS: {e}")

def shutdown():
    try:
        vbs_path = os.path.abspath("shutdown_script.vbs")
        # Формируем аргументы для передачи в VBS
        args = f'"{vbs_path}"'
        subprocess.run(f'cscript {args}', shell=True)
    except Exception as e:
        logger.error(f"Ошибка при запуске VBS: {e}")
