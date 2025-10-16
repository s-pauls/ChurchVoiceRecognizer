import os
import subprocess
from logger import setup_logger

logger = setup_logger(name="actions", log_file="actions.log")

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
