# 🚀 Деплой SendVPN на Render.com

## Шаг 1: Подготовка репозитория

1. Создайте новый репозиторий на GitHub:
   - Перейдите на https://github.com/new
   - Название: `SendVPN`
   - Описание: `Free VPN Aggregator - Telegram Bot + REST API`
   - Сделайте публичным или приватным

2. Загрузите код:

```bash
cd C:\Users\Xsiwo\Desktop\efgdsj\SendVPN
git init
git add .
git commit -m "Initial commit: SendVPN Bot + API"
git branch -M main
git remote add origin https://github.com/Xsiwo/SendVPN.git
git push -u origin main
```

## Шаг 2: Деплой на Render.com

### Вариант A: Через Blueprint (автоматический)

1. Перейдите на https://dashboard.render.com/blueprints
2. Нажмите **"New Blueprint Instance"**
3. Подключите ваш GitHub репозиторий `Xsiwo/SendVPN`
4. Render автоматически обнаружит `render.yaml`
5. Укажите переменные окружения:
   - `BOT_TOKEN` — токен от @BotFather
   - `ADMIN_IDS` — ваш Telegram ID

6. Нажмите **"Apply"**

Render создаст:
- ✅ Web Service (API + Bot)
- ✅ PostgreSQL Database
- ✅ Автоматические деплои при push

### Вариант B: Вручную

#### 1. Создать PostgreSQL базу данных

1. Перейдите в https://dashboard.render.com/
2. **"New +"** → **"PostgreSQL"**
3. Настройки:
   - Name: `sendvpn-db`
   - Database: `sendvpn`
   - User: `sendvpn`
   - Region: `Frankfurt` (ближайший к России)
   - Plan: `Free`

4. Нажмите **"Create Database"**
5. Скопируйте **Internal Database URL** (начинается с `postgresql://`)

#### 2. Создать Web Service

1. **"New +"** → **"Web Service"**
2. Подключите ваш GitHub репозиторий
3. Настройки:
   - Name: `sendvpn-api`
   - Region: `Frankfurt`
   - Branch: `main`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

4. **Environment Variables:**
   ```
   MODE=all
   PORT=10000
   BOT_TOKEN=ваш_токен_от_BotFather
   ADMIN_IDS=ваш_telegram_id
   DATABASE_URL=скопированный_Internal_Database_URL
   LOG_LEVEL=INFO
   PARSER_INTERVAL=3600
   ```

5. Plan: `Free`
6. Нажмите **"Create Web Service"**

## Шаг 3: Проверка

После деплоя (занимает 5-10 минут):

1. **API**: Откройте `https://sendvpn-api.onrender.com/`
2. **Документация**: `https://sendvpn-api.onrender.com/api/docs`
3. **Telegram бот**: Напишите вашему боту `/start`

## Endpoints API

### Получить категории
```bash
GET https://sendvpn-api.onrender.com/api/categories
```

### Получить протоколы
```bash
GET https://sendvpn-api.onrender.com/api/protocols?category=v2ray
```

### Получить серверы
```bash
GET https://sendvpn-api.onrender.com/api/servers?protocol=vmess&limit=10
```

### Случайный сервер
```bash
GET https://sendvpn-api.onrender.com/api/servers/random?protocol=vless
```

### Статистика
```bash
GET https://sendvpn-api.onrender.com/api/stats
```

### Список стран
```bash
GET https://sendvpn-api.onrender.com/api/countries
```

## Важные замечания

### Бесплатный план Render.com
- ✅ 750 часов/месяц бесплатно
- ✅ Автоматический HTTPS
- ✅ PostgreSQL 1GB бесплатно
- ⚠️ Засыпает после 15 минут неактивности
- ⚠️ Холодный старт ~30 секунд

### Чтобы избежать засыпания:
1. Используйте UptimeRobot (https://uptimerobot.com/)
2. Пингуйте `/health` каждые 5 минут
3. Или перейдите на платный план ($7/мес)

### Логи
Смотрите логи в реальном времени:
```
Render Dashboard → Your Service → Logs
```

### Обновления
При каждом `git push` в main — автоматический деплой!

## Тестирование локально

```bash
# Установить зависимости
pip install -r requirements.txt

# Запустить только API
set MODE=api
python main.py

# Запустить только бота
set MODE=bot
python run.py

# Запустить всё
set MODE=all
python main.py
```

API будет доступен: http://localhost:8000
Документация: http://localhost:8000/api/docs

## Следующие шаги

1. ✅ Получить токен от @BotFather
2. ✅ Залить код на GitHub
3. ✅ Задеплоить на Render.com
4. ✅ Проверить работу API и бота
5. ⏭️ Создать Android-приложение

## Поддержка

Проблемы? Напишите в Telegram: @Xsiwo
