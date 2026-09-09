#!/bin/bash

echo "🚀 Запуск SendVPN бота..."

# Активация виртуального окружения
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Виртуальное окружение не найдено!"
    echo "Запустите ./install.sh сначала."
    exit 1
fi

# Проверка .env
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "Скопируйте .env.example в .env и заполните данные."
    exit 1
fi

# Запуск бота
echo "✅ Запуск бота..."
python run.py
