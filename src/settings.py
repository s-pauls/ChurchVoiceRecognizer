"""
Модуль для управления настройками приложения
"""
import json
import os
from typing import Dict, Any, Optional


class SettingsManager:
    def __init__(self, config_file: str = "settings.json"):
        self.config_file = config_file
        self.default_settings = {
            "audio_device_name": "",
            "last_updated": None
        }
        
    def load_settings(self) -> Dict[str, Any]:
        """Загружает настройки из файла или возвращает настройки по умолчанию"""
        if not os.path.exists(self.config_file):
            return self.default_settings.copy()
            
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # Объединяем с настройками по умолчанию для новых ключей
                merged_settings = self.default_settings.copy()
                merged_settings.update(settings)
                return merged_settings
        except (json.JSONDecodeError, FileNotFoundError, Exception) as e:
            print(f"⚠️ Ошибка загрузки настроек: {e}")
            return self.default_settings.copy()
            
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Сохраняет настройки в файл"""
        try:
            from datetime import datetime
            settings["last_updated"] = datetime.now().isoformat()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"⚠️ Ошибка сохранения настроек: {e}")
            return False

        
    def save_audio_device(self, device_name: str = "") -> bool:
        """Сохраняет выбранное аудио устройство"""
        settings = self.load_settings()
        settings["audio_device_name"] = device_name
        return self.save_settings(settings)

    def save_complete_settings(self, device_name: str) -> bool:
        """Сохраняет все настройки за один раз"""
        settings = self.load_settings()
        settings.update({
            #"audio_device_index": device_index,
            "audio_device_name": device_name,
            #"service_type": service_type
        })
        return self.save_settings(settings)
        
    def reset_settings(self) -> bool:
        """Сбрасывает настройки к значениям по умолчанию"""
        return self.save_settings(self.default_settings.copy())


# Глобальный экземпляр менеджера настроек
settings_manager = SettingsManager()


def load_settings() -> Dict[str, Any]:
    """Удобная функция для загрузки настроек"""
    return settings_manager.load_settings()


def save_settings(device_name: str) -> bool:
    """Удобная функция для сохранения настроек"""
    return settings_manager.save_complete_settings(device_name)


if __name__ == "__main__":
    # Тестирование модуля
    print("Тестирование модуля настроек...")
    
    # Загружаем текущие настройки
    settings = load_settings()
    print(f"Текущие настройки: {settings}")
    
    # Сохраняем тестовые настройки
    if save_settings("Test Device"):
        print("✅ Настройки сохранены")
    else:
        print("❌ Ошибка сохранения")
        
    # Загружаем снова для проверки
    updated_settings = load_settings()
    print(f"Обновленные настройки: {updated_settings}")