# 📋 Быстрая инструкция по запуску SendVPN

## Windows

### Быстрый старт (через скрипты)

1. Откройте проект в проводнике
2. Запустите `install.bat` (установка)
3. Отредактируйте файл `.env` - добавьте токен бота
4. Запустите `start.bat`

### Ручная установка

```bash
# 1. Создать виртуальное окружение
python -m venv venv

# 2. Активировать
venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать .env файл
copy .env.example .env

# 5. Отредактировать .env и добавить BOT_TOKEN

# 6. Запустить
python run.py
```

## Linux / macOS

### Быстрый старт (через скрипты)

```bash
# 1. Установка
chmod +x install.sh
./install.sh

# 2. Редактировать .env
nano .env

# 3. Запуск
chmod +x start.sh
./start.sh
```

### Ручная установка

```bash
# 1. Создать виртуальное окружение
python3 -m venv venv

# 2. Активировать
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать .env файл
cp .env.example .env

# 5. Отредактировать .env
nano .env

# 6. Запустить
python run.py
```

## Docker

```bash
# 1. Создать .env файл
cp .env.example .env

# 2. Отредактировать .env
nano .env

# 3. Запустить
docker-compose up -d

# 4. Посмотреть логи
docker-compose logs -f
```

## Получение токена бота

1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен в `.env` файл

## Получение Admin ID

1. Найдите [@userinfobot](https://t.me/userinfobot) в Telegram
2. Отправьте `/start`
3. Скопируйте ваш ID в `.env` файл

## Структура .env

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz    # От @BotFather
ADMIN_IDS=123456789                                 # Ваш Telegram ID
DATABASE_URL=sqlite+aiosqlite:///data/sendvpn.db   # Путь к БД
PARSER_INTERVAL=3600                                # Интервал парсинга (сек)
LOG_LEVEL=INFO                                      # Уровень логов
```

## Возможные проблемы

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Permission denied (Linux/Mac)
```bash
chmod +x install.sh start.sh
```

### Бот не отвечает
- Проверьте токен в `.env`
- Проверьте интернет соединение
- Посмотрите логи: `logs/sendvpn.log`

## Команды бота

- `/start` - Запуск бота
- `/help` - Помощь
- `/stats` - Статистика
- `/donate` - Поддержать проект

## Поддержка

- Telegram: @sendvpn_support
- GitHub Issues: [github.com/yourusername/SendVPN/issues](https://github.com/yourusername/SendVPN/issues)
