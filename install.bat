@echo off
echo Установка ChurchVoiceRecognizer...

echo.
echo Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден!
    echo Пожалуйста, установите Python с https://www.python.org/downloads/
    echo Не забудьте отметить "Add Python to PATH" при установке
    pause
    exit /b 1
)

echo Python найден!

echo.
echo Обновление pip...
python -m pip install --upgrade pip

echo.
echo Попытка установки зависимостей...
echo Пробуем стандартные зависимости...
python -m pip install -r requirements.txt


echo.
echo Установка завершена!
echo Для запуска используйте: cd src && python main.py
pause