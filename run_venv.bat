@echo off
chcp 65001 >nul
setlocal

echo ========================================
echo   Запуск ChurchVoiceRecognizer (venv)
echo ========================================
echo.

:: Получение текущего каталога
set "PROJECT_DIR=%~dp0"
echo Рабочий каталог: %PROJECT_DIR%

:: Проверка и активация виртуального окружения
if exist "%PROJECT_DIR%.venv\Scripts\activate.bat" (
    echo Найдено виртуальное окружение, активируем...
    call "%PROJECT_DIR%.venv\Scripts\activate.bat"
    if %errorlevel% neq 0 (
        echo ОШИБКА: Не удается активировать виртуальное окружение!
        pause
        exit /b 1
    )
    echo Виртуальное окружение активировано
) else (
    echo Виртуальное окружение не найдено, используем системный Python
)

:: Проверка наличия Python
echo Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден!
    echo Пожалуйста, установите Python или выполните install.bat
    pause
    exit /b 1
)


:: Проверка наличия main.py
if not exist "src\main.py" (
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
python src\main.py

echo.
echo ----------------------------------------
if %errorlevel% neq 0 (
    echo Приложение завершилось с ошибкой (код: %errorlevel%)
) else (
    echo Приложение завершено успешно
)

echo.