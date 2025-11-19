"""
Модуль для отправки горячих клавиш в OBS64.exe
Использует Windows API для надежной отправки клавиш
Поддерживает сочетания с любыми буквами A-Z: CTRL+SHIFT+[A-Z], CTRL+ALT+[A-Z], etc.
Примеры: CTRL+SHIFT+T, CTRL+SHIFT+B, CTRL+SHIFT+A, CTRL+ALT+F, и т.д.
"""

import time
import psutil
import ctypes
from ctypes import wintypes
import sys
from typing import Optional, List

# Импорт Windows API функций
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Константы виртуальных клавиш
VK_CONTROL = 0x11
VK_SHIFT = 0x10
VK_LCONTROL = 0xA2
VK_LSHIFT = 0xA0

# Буквы A-Z (виртуальные коды совпадают с ASCII)
VK_A = 0x41
VK_B = 0x42
VK_C = 0x43
VK_D = 0x44
VK_E = 0x45
VK_F = 0x46
VK_G = 0x47
VK_H = 0x48
VK_I = 0x49
VK_J = 0x4A
VK_K = 0x4B
VK_L = 0x4C
VK_M = 0x4D
VK_N = 0x4E
VK_O = 0x4F
VK_P = 0x50
VK_Q = 0x51
VK_R = 0x52
VK_S = 0x53
VK_T = 0x54
VK_U = 0x55
VK_V = 0x56
VK_W = 0x57
VK_X = 0x58
VK_Y = 0x59
VK_Z = 0x5A

# Константы для событий клавиатуры
KEYEVENTF_KEYUP = 0x0002
SW_RESTORE = 9

# Определение структур для Windows API
class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]

# Декларация Windows API функций
user32.FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
user32.FindWindowW.restype = wintypes.HWND

user32.SetForegroundWindow.argtypes = [wintypes.HWND]
user32.SetForegroundWindow.restype = wintypes.BOOL

user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
user32.ShowWindow.restype = wintypes.BOOL

user32.keybd_event.argtypes = [wintypes.BYTE, wintypes.BYTE, wintypes.DWORD, ctypes.POINTER(wintypes.ULONG)]
user32.keybd_event.restype = None

user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
user32.GetWindowThreadProcessId.restype = wintypes.DWORD


class OBSHotkeyManager:
    """Класс для управления горячими клавишами OBS"""
    
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
    
    def get_obs_window_handle(self) -> Optional[int]:
        """Получение handle главного окна OBS"""
        obs_process = self.find_obs_process()
        if not obs_process:
            return None
            
        try:
            windows = []

            # Ищем окна, принадлежащие процессу OBS
            def enum_windows_callback(hwnd, lparam):
                if user32.IsWindowVisible(hwnd):
                    process_id = wintypes.DWORD()
                    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
                    if process_id.value == obs_process.pid:
                        # Получаем заголовок окна
                        length = user32.GetWindowTextLengthW(hwnd)
                        if length > 0:
                            buffer = ctypes.create_unicode_buffer(length + 1)
                            user32.GetWindowTextW(hwnd, buffer, length + 1)
                            # Ищем главное окно OBS (обычно содержит "OBS" в заголовке)
                            if "OBS" in buffer.value:
                                windows.append(hwnd)
                return True
            

            WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
            user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)
            
            return windows[0] if windows else None
            
        except Exception as e:
            print(f"Ошибка при поиске окна OBS: {e}")
            return None
    
    def activate_obs_window(self, hwnd: int) -> bool:
        """Активация окна OBS"""
        try:
            # Восстанавливаем окно если оно свернуто
            user32.ShowWindow(hwnd, SW_RESTORE)
            time.sleep(0.1)
            
            # Выносим окно на передний план
            result = user32.SetForegroundWindow(hwnd)
            time.sleep(0.2)  # Даем время для активации
            
            return bool(result)
        except Exception as e:
            print(f"Ошибка при активации окна OBS: {e}")
            return False
    
    def send_key_combination(self, ctrl: bool = False, shift: bool = False, alt: bool = False, key_code: int = None):
        """Отправка комбинации клавиш через Windows API"""
        if key_code is None:
            print("Ошибка: key_code не определен")
            return False
            
        try:
            modifiers_text = []
            if ctrl: modifiers_text.append("CTRL")
            if shift: modifiers_text.append("SHIFT") 
            if alt: modifiers_text.append("ALT")
            
            print(f"Отправляем комбинацию: {'+'.join(modifiers_text)}+{chr(key_code)} (код {key_code})")
            
            # Нажимаем модификаторы
            if ctrl:
                user32.keybd_event(VK_LCONTROL, 0, 0, None)
            if shift:
                user32.keybd_event(VK_LSHIFT, 0, 0, None)
            if alt:
                user32.keybd_event(0x12, 0, 0, None)  # VK_MENU (Alt)
            
            time.sleep(0.05)
            
            # Нажимаем основную клавишу
            user32.keybd_event(key_code, 0, 0, None)
            time.sleep(0.05)
            
            # Отпускаем основную клавишу
            user32.keybd_event(key_code, 0, KEYEVENTF_KEYUP, None)
            
            time.sleep(0.05)
            
            # Отпускаем модификаторы в обратном порядке
            if alt:
                user32.keybd_event(0x12, 0, KEYEVENTF_KEYUP, None)
            if shift:
                user32.keybd_event(VK_LSHIFT, 0, KEYEVENTF_KEYUP, None)
            if ctrl:
                user32.keybd_event(VK_LCONTROL, 0, KEYEVENTF_KEYUP, None)
                
            return True
            
        except Exception as e:
            print(f"Ошибка при отправке клавиш: {e}")
            return False
    
    def send_hotkey_to_obs(self, hotkey_string: str) -> bool:
        """Отправка горячих клавиш в OBS по строковому описанию"""
        
        # Проверяем, запущен ли OBS
        if not self.find_obs_process():
            print("Ошибка: OBS64.exe не запущен!")
            return False

        # Получаем handle окна OBS
        hwnd = self.get_obs_window_handle()
        if not hwnd:
            print("Ошибка: Не удалось найти окно OBS!")
            return False

        # Активируем окно OBS
        if not self.activate_obs_window(hwnd):
            print("Предупреждение: Не удалось активировать окно OBS, но продолжаем...")
        
        # Парсим комбинацию клавиш
        hotkey_upper = hotkey_string.upper()
        
        # Определяем модификаторы и основную клавишу
        ctrl = "CTRL" in hotkey_upper
        shift = "SHIFT" in hotkey_upper
        alt = "ALT" in hotkey_upper
        
        # Создаем словарь соответствия букв и их виртуальных кодов
        key_map = {
            'A': VK_A, 'B': VK_B, 'C': VK_C, 'D': VK_D, 'E': VK_E,
            'F': VK_F, 'G': VK_G, 'H': VK_H, 'I': VK_I, 'J': VK_J,
            'K': VK_K, 'L': VK_L, 'M': VK_M, 'N': VK_N, 'O': VK_O,
            'P': VK_P, 'Q': VK_Q, 'R': VK_R, 'S': VK_S, 'T': VK_T,
            'U': VK_U, 'V': VK_V, 'W': VK_W, 'X': VK_X, 'Y': VK_Y,
            'Z': VK_Z
        }
        
        # Находим последнюю букву в строке (основную клавишу)
        key_code = None
        for letter in key_map:
            if f"+{letter}" in hotkey_upper:
                key_code = key_map[letter]
                break
        
        if key_code is None:
            print(f"Неподдерживаемая комбинация клавиш: {hotkey_string}")
            return False
        
        print(f"Отправка {hotkey_string} в OBS...")
        return self.send_key_combination(ctrl, shift, alt, key_code)

    def send_ctrl_shift_a(self) -> bool:
        """Отправка CTRL+SHIFT+A"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+A")

    def send_ctrl_shift_b(self) -> bool:
        """Отправка CTRL+SHIFT+B"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+B")

    def send_ctrl_shift_d(self) -> bool:
        """Отправка CTRL+SHIFT+D"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+D")

    def send_ctrl_shift_e(self) -> bool:
        """Отправка CTRL+SHIFT+E"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+E")

    def send_ctrl_shift_f(self) -> bool:
        """Отправка CTRL+SHIFT+F"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+F")

    def send_ctrl_shift_g(self) -> bool:
        """Отправка CTRL+SHIFT+G"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+G")

    def send_ctrl_shift_h(self) -> bool:
        """Отправка CTRL+SHIFT+H"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+H")

    def send_ctrl_shift_i(self) -> bool:
        """Отправка CTRL+SHIFT+I"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+I")

    def send_ctrl_shift_j(self) -> bool:
        """Отправка CTRL+SHIFT+J"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+J")

    def send_ctrl_shift_m(self) -> bool:
        """Отправка CTRL+SHIFT+M"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+M")

    def send_ctrl_shift_o(self) -> bool:
        """Отправка CTRL+SHIFT+O"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+O")

    def send_ctrl_shift_p(self) -> bool:
        """Отправка CTRL+SHIFT+P"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+P")
    
    def send_ctrl_shift_r(self) -> bool:
        """Отправка CTRL+SHIFT+R"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+R")
    
    def send_ctrl_shift_s(self) -> bool:
        """Отправка CTRL+SHIFT+S"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+S")

    def send_ctrl_shift_t(self) -> bool:
        """Отправка CTRL+SHIFT+T"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+T")

    def send_ctrl_shift_u(self) -> bool:
        """Отправка CTRL+SHIFT+U"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+U")

    def send_ctrl_shift_x(self) -> bool:
        """Отправка CTRL+SHIFT+X"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+X")

    def send_ctrl_shift_y(self) -> bool:
        """Отправка CTRL+SHIFT+Y"""
        return self.send_hotkey_to_obs("CTRL+SHIFT+Y")

def main():
    """Основная функция"""
    manager = OBSHotkeyManager()
    
    if len(sys.argv) > 1:
        # Используем аргумент командной строки
        hotkey = sys.argv[1]
        success = manager.send_hotkey_to_obs(hotkey)
        if success:
            print(f"Горячие клавиши {hotkey} успешно отправлены в OBS!")
        else:
            print(f"Не удалось отправить горячие клавиши {hotkey}")
    else:
        # Демонстрация всех поддерживаемых комбинаций
        print("Демонстрация отправки горячих клавиш в OBS...")
        print("Поддерживаются любые комбинации с буквами A-Z:")
        print("- CTRL+SHIFT+[A-Z] (например: CTRL+SHIFT+T, CTRL+SHIFT+B)")
        print("- CTRL+ALT+[A-Z] (например: CTRL+ALT+F, CTRL+ALT+G)")
        print("- SHIFT+ALT+[A-Z], и другие комбинации модификаторов")
        print()
        
        hotkeys = ["CTRL+SHIFT+O", "CTRL+SHIFT+M", "CTRL+SHIFT+A",
                  "CTRL+SHIFT+K", "CTRL+SHIFT+B"]
        
        for hotkey in hotkeys:
            print(f"Отправка {hotkey}...")
            success = manager.send_hotkey_to_obs(hotkey)
            if success:
                print(f"✓ {hotkey} успешно отправлено")
            else:
                print(f"✗ Ошибка при отправке {hotkey}")
            print()
            time.sleep(3)


if __name__ == "__main__":
    main()