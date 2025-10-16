"""
Модуль для создания графического интерфейса настроек приложения
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sounddevice as sd
from audio_device import list_input_devices
from settings import load_settings


class SettingsDialog:
    def __init__(self, parent=None):
        self.result = None
        self.selected_device = None
        self.selected_service = None
        
        # Загружаем сохраненные настройки
        self.saved_settings = load_settings()
        
        # Создаем главное окно
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title("🎙️ Настройки службы")
        self.root.geometry("450x300")
        self.root.resizable(False, False)
        
        # Центрируем окно
        self.center_window()
        
        # Делаем окно модальным
        self.root.transient(parent)
        self.root.grab_set()
        
        self.setup_ui()
        
    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        pos_x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        
    def setup_ui(self):
        """Создает элементы интерфейса"""
        # Заголовок
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=20)
        
        title_label = ttk.Label(
            title_frame, 
            text="⛪ Настройки системы распознавания речи",
            font=("Arial", 14, "bold")
        )
        title_label.pack()
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=30, pady=10, fill="both", expand=True)
        
        # Выбор типа службы
        service_frame = ttk.LabelFrame(main_frame, text="📜 Тип службы", padding=10)
        service_frame.pack(fill="x", pady=(0, 15))
        
        # Устанавливаем сохраненный тип службы
        saved_service = self.saved_settings.get("service_type", "литургия")
        self.service_var = tk.StringVar(value=saved_service)
        
        ttk.Radiobutton(
            service_frame, 
            text="🕊️ Божественная Литургия", 
            variable=self.service_var, 
            value="литургия"
        ).pack(anchor="w", pady=2)
        
        ttk.Radiobutton(
            service_frame, 
            text="🌟 Всенощное бдение", 
            variable=self.service_var, 
            value="всенощная"
        ).pack(anchor="w", pady=2)
        
        # Выбор аудио устройства
        device_frame = ttk.LabelFrame(main_frame, text="🎤 Микрофон", padding=10)
        device_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(device_frame, text="Выберите устройство записи:").pack(anchor="w", pady=(0, 5))
        
        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(
            device_frame, 
            textvariable=self.device_var, 
            state="readonly",
            width=50
        )
        self.device_combo.pack(fill="x", pady=(0, 5))
        
        # Загружаем список устройств
        self.load_audio_devices()
        
        # Кнопка обновления устройств
        refresh_btn = ttk.Button(
            device_frame, 
            text="🔄 Обновить список", 
            command=self.load_audio_devices
        )
        refresh_btn.pack(anchor="e", pady=(5, 0))
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(
            button_frame, 
            text="❌ Отмена", 
            command=self.cancel
        ).pack(side="right", padx=(10, 0))
        
        ttk.Button(
            button_frame, 
            text="✅ Запустить службу", 
            command=self.ok,
            style="Accent.TButton"
        ).pack(side="right")
        
        # Привязываем Enter к OK
        self.root.bind('<Return>', lambda e: self.ok())
        self.root.bind('<Escape>', lambda e: self.cancel())
        
    def load_audio_devices(self):
        """Загружает список доступных аудио устройств"""
        try:
            devices = sd.query_devices()
            input_devices = list_input_devices()
            
            device_options = []
            saved_device_index = self.saved_settings.get("audio_device_index")
            
            for i in input_devices:
                device_name = devices[i]['name']
                device_options.append(f"{i}: {device_name}")
            
            self.device_combo['values'] = device_options
            
            if device_options:
                # Попытаемся выбрать сохраненное устройство
                selected_index = 0
                if saved_device_index is not None:
                    for idx, option in enumerate(device_options):
                        if option.startswith(f"{saved_device_index}:"):
                            selected_index = idx
                            break
                
                self.device_combo.current(selected_index)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить аудио устройства:\n{e}")
            
    def ok(self):
        """Обработчик кнопки OK"""
        if not self.device_var.get():
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите микрофон")
            return
            
        # Извлекаем индекс устройства из строки "index: name"
        device_text = self.device_var.get()
        try:
            device_index = int(device_text.split(':')[0])
            self.selected_device = device_index
            self.selected_service = self.service_var.get()
            self.result = True
            self.root.destroy()
        except (ValueError, IndexError):
            messagebox.showerror("Ошибка", "Неверный формат выбранного устройства")
            
    def cancel(self):
        """Обработчик кнопки Отмена"""
        self.result = False
        self.root.destroy()
        
    def show(self):
        """Показывает диалог и возвращает результат"""
        self.root.focus_set()
        self.root.wait_window()
        return self.result


def show_settings_dialog():
    """
    Показывает диалог настроек и возвращает кортеж (device_index, service_type)
    Возвращает None, если пользователь отменил действие
    """
    dialog = SettingsDialog()
    if dialog.show():
        return dialog.selected_device, dialog.selected_service
    return None


if __name__ == "__main__":
    # Тест диалога
    result = show_settings_dialog()
    if result:
        device_index, service_type = result
        print(f"Выбрано устройство: {device_index}, служба: {service_type}")
    else:
        print("Настройка отменена")