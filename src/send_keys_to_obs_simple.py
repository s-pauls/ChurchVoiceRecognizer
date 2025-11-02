"""
Упрощенная версия для отправки горячих клавиш в OBS
Использует библиотеку keyboard для более простой работы
Требует установки: pip install keyboard psutil
"""

import time
import psutil
import sys
from typing import Optional

try:
    import keyboard
except ImportError:
    print("Ошибка: Не найдена библиотека keyboard")
    print("Установите её командой: pip install keyboard")
    sys.exit(1)

try:
    import win32gui
    import win32con
    import win32process
except ImportError:
    print("Ошибка: Не найдена библиотека pywin32")
    print("Установите её командой: pip install pywin32")
    sys.exit(1)


class OBSHotkeySimple:
    """Упрощенный класс для отправки горячих клавиш в OBS"""
    
    def __init__(self):
        self.obs_process_name = "obs64.exe"
        
    def find_obs_process(self) -> Optional[psutil.Process]:
        """Поиск процесса OBS64.exe"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == self.obs_process_name.lower():
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        return None
    
    def get_obs_windows(self) -> list:
        """Получение всех окон OBS"""
        obs_process = self.find_obs_process()
        if not obs_process:
            return []
        
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                _, process_id = win32process.GetWindowThreadProcessId(hwnd)
                if process_id == obs_process.pid:
                    window_title = win32gui.GetWindowText(hwnd)
                    if window_title and "OBS" in window_title:
                        windows.append((hwnd, window_title))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        return windows
    
    def activate_obs_window(self) -> bool:
        """Активация главного окна OBS"""
        obs_windows = self.get_obs_windows()
        if not obs_windows:
            print("Не найдено окон OBS")
            return False
        
        # Берем первое найденное окно OBS
        hwnd, title = obs_windows[0]
        
        try:
            # Восстанавливаем окно если свернуто
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(0.1)
            
            # Выносим на передний план
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.3)  # Даем время для активации
            
            print(f"Активировано окно: {title}")
            return True
            
        except Exception as e:
            print(f"Ошибка при активации окна OBS: {e}")
            return False
    
    def send_hotkey(self, hotkey_string: str) -> bool:
        """Отправка горячих клавиш через библиотеку keyboard"""
        
        # Проверяем, запущен ли OBS
        if not self.find_obs_process():
            print("Ошибка: OBS64.exe не запущен!")
            return False
        
        # Активируем окно OBS
        if not self.activate_obs_window():
            print("Предупреждение: Не удалось активировать окно OBS")
        
        try:
            print(f"Отправка комбинации: {hotkey_string}")
            
            # Конвертируем в формат библиотеки keyboard
            hotkey_formatted = hotkey_string.lower().replace('+', '+')
            
            # Отправляем комбинацию клавиш
            keyboard.send(hotkey_formatted)
            
            print(f"✓ Комбинация {hotkey_string} успешно отправлена")
            return True
            
        except Exception as e:
            print(f"Ошибка при отправке клавиш: {e}")
            return False
    
    def send_ctrl_shift_t(self) -> bool:
        """Отправка CTRL+SHIFT+T"""
        return self.send_hotkey("ctrl+shift+t")
    
    def send_ctrl_shift_b(self) -> bool:
        """Отправка CTRL+SHIFT+B"""
        return self.send_hotkey("ctrl+shift+b")
    
    def send_ctrl_shift_a(self) -> bool:
        """Отправка CTRL+SHIFT+A"""
        return self.send_hotkey("ctrl+shift+a")
    
    def send_ctrl_shift_x(self) -> bool:
        """Отправка CTRL+SHIFT+X"""
        return self.send_hotkey("ctrl+shift+x")
    
    def send_ctrl_shift_p(self) -> bool:
        """Отправка CTRL+SHIFT+P"""
        return self.send_hotkey("ctrl+shift+p")
    
    def send_ctrl_shift_d(self) -> bool:
        """Отправка CTRL+SHIFT+D"""
        return self.send_hotkey("ctrl+shift+d")
    
    def send_ctrl_shift_h(self) -> bool:
        """Отправка CTRL+SHIFT+H"""
        return self.send_hotkey("ctrl+shift+h")


def main():
    """Основная функция"""
    manager = OBSHotkeySimple()
    
    if len(sys.argv) > 1:
        # Используем аргумент командной строки
        hotkey = sys.argv[1].lower()
        success = manager.send_hotkey(hotkey)
        if not success:
            print(f"Не удалось отправить горячие клавиши: {hotkey}")
    else:
        # Демонстрация
        print("=== Отправка горячих клавиш в OBS ===")
        print("Поддерживаемые комбинации:")
        print("- ctrl+shift+t")
        print("- ctrl+shift+b") 
        print("- ctrl+shift+a")
        print("- ctrl+shift+x")
        print("- ctrl+shift+p")
        print("- ctrl+shift+d")
        print("- ctrl+shift+h")
        print()
        
        # Проверяем наличие OBS
        if not manager.find_obs_process():
            print("OBS64.exe не запущен!")
            return
        
        # Тестируем все комбинации
        hotkeys = ["ctrl+shift+t", "ctrl+shift+b", "ctrl+shift+a", 
                  "ctrl+shift+x", "ctrl+shift+p", "ctrl+shift+d", "ctrl+shift+h"]
        
        for hotkey in hotkeys:
            print(f"Тестирование {hotkey}...")
            manager.send_hotkey(hotkey)
            time.sleep(2)  # Пауза между отправками
        
        print("Тестирование завершено!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрервано пользователем")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()