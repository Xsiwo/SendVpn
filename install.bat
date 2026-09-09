@echo off
echo ================================================
echo    Установка SendVPN для Windows
echo ================================================
echo.

REM Проверка Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python не установлен!
    echo Скачайте Python 3.11+ с https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Создание виртуального окружения...
python -m venv venv

echo [2/5] Активация окружения...
call venv\Scripts\activate.bat

echo [3/5] Обновление pip...
python -m pip install --upgrade pip

echo [4/5] Установка зависимостей...
pip install -r requirements.txt

echo [5/5] Создание директорий...
if not exist "data" mkdir data
if not exist "logs" mkdir logs

REM Копирование .env
if not exist ".env" (
    echo.
    echo Создание .env файла...
    copy .env.example .env
    echo.
    echo ВАЖНО: Не забудьте отредактировать .env файл!
)

echo.
echo ================================================
echo    Установка завершена успешно!
echo ================================================
echo.
echo Следующие шаги:
echo 1. Отредактируйте .env файл и добавьте BOT_TOKEN
echo 2. Запустите: start.bat
echo.
pause
