@echo off
setlocal

echo ========================================
echo   Запуск ChurchVoiceRecognizer
echo ========================================
echo.

:: Проверка наличия Python
echo Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден!
    echo Пожалуйста, установите Python или выполните install.bat
    pause
    exit /b 1
)

:: Получение текущего каталога
set "PROJECT_DIR=%~dp0"
echo Рабочий каталог: %PROJECT_DIR%

:: Переход в папку src
echo Переход в папку src...
cd /d "%PROJECT_DIR%src"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удается найти папку src!
    pause
    exit /b 1
)

:: Проверка наличия main.py
if not exist "main.py" (
    echo ОШИБКА: Файл main.py не найден в папке src!
    pause
    exit /b 1
)

:: Проверка наличия модели
if not exist "%PROJECT_DIR%models" (
    echo ПРЕДУПРЕЖДЕНИЕ: Папка models не найдена!
    echo Убедитесь, что модель Vosk установлена правильно.
    echo.
)

echo.
echo Запуск приложения...
echo ----------------------------------------
python main.py

echo.
echo ----------------------------------------
if %errorlevel% neq 0 (
    echo Приложение завершилось с ошибкой (код: %errorlevel%)
) else (
    echo Приложение завершено успешно
)

echo.
pause