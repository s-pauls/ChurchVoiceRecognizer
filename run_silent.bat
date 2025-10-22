@echo off
chcp 65001 >nul
setlocal

:: Проверка параметра для тихого режима
set "SILENT_MODE=%1"

if not "%SILENT_MODE%"=="silent" (
    echo ========================================
    echo   Запуск ChurchVoiceRecognizer (venv)
    echo ========================================
    echo.
)

:: Получение текущего каталога
set "PROJECT_DIR=%~dp0"
if not "%SILENT_MODE%"=="silent" (
    echo Рабочий каталог: %PROJECT_DIR%
)

:: Проверка и активация виртуального окружения
if exist "%PROJECT_DIR%.venv\Scripts\activate.bat" (
    if not "%SILENT_MODE%"=="silent" (
        echo Найдено виртуальное окружение, активируем...
    )
    call "%PROJECT_DIR%.venv\Scripts\activate.bat" >nul 2>&1
    if %errorlevel% neq 0 (
        if not "%SILENT_MODE%"=="silent" (
            echo ОШИБКА: Не удается активировать виртуальное окружение!
            pause
        )
        exit /b 1
    )
    if not "%SILENT_MODE%"=="silent" (
        echo Виртуальное окружение активировано
    )
) else (
    if not "%SILENT_MODE%"=="silent" (
        echo Виртуальное окружение не найдено, используем системный Python
    )
)

:: Проверка наличия Python
if not "%SILENT_MODE%"=="silent" (
    echo Проверка Python...
)
python --version >nul 2>&1
if %errorlevel% neq 0 (
    if not "%SILENT_MODE%"=="silent" (
        echo ОШИБКА: Python не найден!
        echo Пожалуйста, установите Python или выполните install.bat
        pause
    )
    exit /b 1
)

:: Проверка наличия main.py
if not exist "src\main.py" (
    if not "%SILENT_MODE%"=="silent" (
        echo ОШИБКА: Файл main.py не найден в папке src!
        pause
    )
    exit /b 1
)

:: Проверка наличия модели
if not exist "%PROJECT_DIR%models" (
    if not "%SILENT_MODE%"=="silent" (
        echo ПРЕДУПРЕЖДЕНИЕ: Папка models не найдена!
        echo Убедитесь, что модель Vosk установлена правильно.
        echo.
    )
)

if not "%SILENT_MODE%"=="silent" (
    echo.
    echo Запуск приложения...
    echo ----------------------------------------
)

:: Запуск Python с логированием ошибок
if "%SILENT_MODE%"=="silent" (
    echo [%date% %time%] Запуск приложения в тихом режиме >> "%PROJECT_DIR%silent_run.log"
    python src/main.py >> "%PROJECT_DIR%silent_run.log" 2>&1
    echo [%date% %time%] Приложение завершено с кодом: %errorlevel% >> "%PROJECT_DIR%silent_run.log"
) else (
    python src/main.py
)

if not "%SILENT_MODE%"=="silent" (
    echo.
    echo ----------------------------------------
    if %errorlevel% neq 0 (
        echo Приложение завершилось с ошибкой (код: %errorlevel%)
    ) else (
        echo Приложение завершено успешно
    )
    echo.
)