import os
import subprocess
from logger import setup_logger

logger = setup_logger(name="actions", log_file="actions.log")


def on_begin():
    print("🚪 Обнаружено 'благословенно царство' — выполняем действие!")
    send_keys_to_obs('^(+(A))')  # Ctrl+Shift+A


def on_prayer():
    print("🙏 Обнаружено 'отче наш' — выполняем действие!")


def on_doors():
    print("🚪 Обнаружено 'двери, двери' — выполняем действие!")
    send_keys_to_obs('^(+(A))')  # Ctrl+Shift+A


def execute_action(action_name):
    actions = {
        "on_prayer": on_prayer,
        "on_doors": on_doors,
        "on_begin": on_begin
    }
    action = actions.get(action_name)
    if action:
        action()


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
