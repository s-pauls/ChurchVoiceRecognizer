# Инструкция по установке ChurchVoiceRecognizer

## Требования

- Python 3.8 или выше
- Windows 10/11
- Микрофон или аудиоустройство

## Пошаговая установка

### 1. Установка Python

1. Скачайте Python с официального сайта: https://www.python.org/downloads/
2. При установке **обязательно** отметьте галочку "Add Python to PATH"
3. Убедитесь, что установка прошла успешно:
   ```powershell
   python --version
   ```

### 2. Клонирование или скачивание проекта

```powershell
git clone https://github.com/s-pauls/ChurchVoiceRecognizer.git
cd ChurchVoiceRecognizer
```

### 3. Создание виртуального окружения (рекомендуется)

```powershell
python -m venv venv
venv\Scripts\activate
```

### 4. Установка зависимостей

#### Стандартная установка:
```powershell
python -m pip install -r requirements.txt
```

#### Если возникают проблемы с sounddevice на Windows:

1. **Обновите pip до последней версии:**
   ```powershell
   python -m pip install --upgrade pip
   ```

2. **Установите Microsoft C++ Build Tools:**
   - Скачайте Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
   - Установите с компонентами "C++ build tools"

3. **Альтернативная установка sounddevice:**
   ```powershell
   # Попробуйте установить из conda-forge (если есть conda)
   conda install -c conda-forge python-sounddevice
   
   # Или попробуйте более новую версию
   python -m pip install sounddevice --upgrade
   
   # Или установите без конкретной версии
   python -m pip install sounddevice
   ```

4. **Установите портфайл отдельно (может помочь):**
   ```powershell
   python -m pip install cffi
   python -m pip install sounddevice
   ```

### 5. Скачивание модели распознавания

Модель Vosk уже включена в проект в папке `models/vosk-model-small-ru-0.22/`

### 6. Запуск приложения

```powershell
cd src
python main.py
```

## Решение проблем

### Проблема: "python не найден"
- Переустановите Python с галочкой "Add Python to PATH"
- Или используйте полный путь к python.exe

### Проблема: "pip не найден"
```powershell
python -m ensurepip --upgrade
python -m pip --version
```

### Проблема: Ошибки компиляции при установке sounddevice
1. Установите Visual Studio Build Tools
2. Перезапустите PowerShell
3. Попробуйте установку снова

### Проблема: Нет доступа к микрофону
- Проверьте разрешения микрофона в настройках Windows
- Запустите приложение от имени администратора

## Альтернативная установка без sounddevice

Если возникают проблемы с sounddevice, создайте файл `requirements-minimal.txt`:

```
vosk==0.3.45
tkinter
```

И используйте альтернативную аудиобиблиотеку:
```powershell
python -m pip install pyaudio
```

Затем в коде замените sounddevice на pyaudio.

## Поддержка

При возникновении проблем:
1. Проверьте версию Python: `python --version`
2. Проверьте установленные пакеты: `python -m pip list`
3. Создайте issue в репозитории с описанием ошибки