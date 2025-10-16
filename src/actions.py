import os
import subprocess
from logger import setup_logger

logger = setup_logger()


def on_begin():
    print("🚪 Обнаружено 'благословенно царство' — выполняем действие!")
    send_keys_to_obs('^(+(A))')  # Ctrl+Shift+A


def on_prayer():
    print("🙏 Обнаружено 'отче наш' — выполняем действие!")


def on_doors():
    print("🚪 Обнаружено 'двери, двери' — выполняем действие!")
    send_keys_to_obs('^(+(A))')  # Ctrl+Shift+A


def on_trisagion():
    print("✝️ Обнаружено 'святый боже' — выполняем действие!")
    send_keys_to_obs('^(+(B))')  # Ctrl+Shift+B


def on_cherubic():
    print("👼 Обнаружено 'херувимская' — выполняем действие!")
    send_keys_to_obs('^(+(C))')  # Ctrl+Shift+C


def on_axion():
    print("🎵 Обнаружено 'достойно есть' — выполняем действие!")
    send_keys_to_obs('^(+(D))')  # Ctrl+Shift+D


# Действия для всенощной
def on_theotokos():
    print("🌟 Обнаружено 'богородице дево' — выполняем действие!")
    send_keys_to_obs('^(+(E))')  # Ctrl+Shift+E


def on_praise():
    print("🎵 Обнаружено 'хвалите имя' — выполняем действие!")
    send_keys_to_obs('^(+(F))')  # Ctrl+Shift+F


def on_magnification():
    print("📿 Обнаружено 'величание' — выполняем действие!")
    send_keys_to_obs('^(+(G))')  # Ctrl+Shift+G


def on_troparion():
    print("🎼 Обнаружено 'тропарь' — выполняем действие!")
    send_keys_to_obs('^(+(H))')  # Ctrl+Shift+H


def on_gloria():
    print("☁️ Обнаружено 'слава в вышних' — выполняем действие!")
    send_keys_to_obs('^(+(I))')  # Ctrl+Shift+I


def execute_action(action_name):
    actions = {
        "on_prayer": on_prayer,
        "on_doors": on_doors,
        "on_begin": on_begin,
        "on_trisagion": on_trisagion,
        "on_cherubic": on_cherubic,
        "on_axion": on_axion,
        "on_theotokos": on_theotokos,
        "on_praise": on_praise,
        "on_magnification": on_magnification,
        "on_troparion": on_troparion,
        "on_gloria": on_gloria
    }
    action = actions.get(action_name)
    if action:
        action()
    else:
        logger.warning(f"Неизвестное действие: {action_name}")


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
