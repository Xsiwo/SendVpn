#!/bin/bash

echo "🚀 Установка SendVPN..."

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не установлен. Установите Python 3.11 или выше."
    exit 1
fi

# Создание виртуального окружения
echo "📦 Создание виртуального окружения..."
python3 -m venv venv

# Активация виртуального окружения
echo "🔄 Активация окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Создание директорий
echo "📁 Создание директорий..."
mkdir -p data logs

# Копирование .env
if [ ! -f .env ]; then
    echo "📝 Создание .env файла..."
    cp .env.example .env
    echo "⚠️  Не забудьте заполнить .env файл своими данными!"
fi

echo ""
echo "✅ Установка завершена!"
echo ""
echo "Следующие шаги:"
echo "1. Отредактируйте .env файл и добавьте BOT_TOKEN"
echo "2. Запустите бота: python run.py"
echo ""
