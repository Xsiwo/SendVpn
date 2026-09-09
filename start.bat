@echo off
echo ================================================
echo         Запуск SendVPN бота
echo ================================================
echo.

REM Активация виртуального окружения
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Виртуальное окружение не найдено!
    echo Запустите install.bat сначала.
    pause
    exit /b 1
)

REM Проверка .env
if not exist ".env" (
    echo Файл .env не найден!
    echo Скопируйте .env.example в .env и заполните данные.
    pause
    exit /b 1
)

REM Запуск бота
echo Запуск бота...
python run.py

pause
