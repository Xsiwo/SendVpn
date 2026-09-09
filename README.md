# SendVPN 🚀

<div align="center">

![SendVPN Logo](https://via.placeholder.com/200x200?text=SendVPN)

**Крупнейший агрегатор бесплатных VPN серверов в Telegram**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.15.0-blue.svg)](https://docs.aiogram.dev/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-@sendvpn__bot-blue.svg)](https://t.me/sendvpn_bot)

</div>

---

## 🌟 Особенности

- 🌍 **70+ VPN протоколов** — все популярные и редкие протоколы
- 📂 **10 категорий** — удобная навигация по типам протоколов
- 🆓 **Полностью бесплатно** — никаких подписок, всё на донатах
- 🔄 **Автообновление** — серверы парсятся каждый час
- 📊 **Статистика** — отслеживание скорости и пинга серверов
- 🌐 **Открытые источники** — GitHub, Telegram, веб-сайты
- 📱 **Инструкции** — помощь по настройке для всех платформ

## 📋 Поддерживаемые протоколы

### 🌟 Основные VPN
WireGuard • OpenVPN • AmneziaWG • IKEv2/IPsec • SoftEther • SSTP • L2TP • PPTP

### 🌐 Прокси
HTTP • HTTPS • SOCKS4 • SOCKS5

### 🥷 Shadowsocks
Shadowsocks • ShadowsocksR • Shadowsocks 2022 • Outline

### ✈️ V2Ray / Xray
VMess • VLESS • Trojan • Trojan-Go

### 🚀 Современные
Brook • Snell • NaiveProxy • Mieru • Juicity

### ⚡ Hysteria / QUIC
Hysteria • Hysteria2 • TUIC

### 🎭 Обфускация
Reality • AnyTLS • ShadowTLS • XHTTP • Vision • obfs4 • meek • Snowflake

### 🧅 Анонимные сети
Tor • I2P • Freenet • Lokinet • Nym • Yggdrasil • CJDNS

### 🌐 DNS протоколы
DoH • DoT • DoQ • DNSCrypt

### 🔑 Туннели
SSH • Stunnel

**И многие другие!**

## 🌐 Live Demo

- **API:** https://sendvpn-api.onrender.com/
- **API Docs:** https://sendvpn-api.onrender.com/api/docs
- **Telegram Bot:** [@sendvpn_bot](https://t.me/sendvpn_bot)

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/Xsiwo/SendVPN.git
cd SendVPN
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и заполните:

```bash
cp .env.example .env
```

Отредактируйте `.env`:
```env
BOT_TOKEN=ваш_токен_бота_от_@BotFather
ADMIN_IDS=ваш_telegram_id
DATABASE_URL=sqlite+aiosqlite:///data/sendvpn.db
```

### 4. Создание директорий

```bash
mkdir -p data logs
```

### 5. Запуск

**Вариант 1: Только Telegram бот**
```bash
set MODE=bot
python run.py
```

**Вариант 2: Только REST API**
```bash
set MODE=api
python main.py
```
API: http://localhost:8000
Документация: http://localhost:8000/api/docs

**Вариант 3: Всё вместе (бот + API)**
```bash
set MODE=all
python main.py
```

## 📁 Структура проекта

```
SendVPN/
├── bot/                    # Telegram бот
│   ├── main.py            # Главный файл бота
│   ├── handlers.py        # Обработчики сообщений
│   └── keyboards.py       # Клавиатуры
├── parsers/               # Парсеры источников
│   ├── base_parser.py    # Базовый парсер
│   ├── github_parser.py  # Парсер GitHub
│   └── web_parser.py     # Парсер веб-сайтов
├── database/              # База данных
│   ├── db.py             # Подключение к БД
│   └── models.py         # Модели данных
├── config/                # Конфигурация
│   └── protocols.py      # Все протоколы
├── utils/                 # Утилиты
│   ├── server_manager.py # Управление серверами
│   └── scheduler.py      # Планировщик задач
├── data/                  # Данные (БД)
├── logs/                  # Логи
├── .env                   # Переменные окружения
├── requirements.txt       # Зависимости
└── README.md             # Документация
```

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | Обязательная |
|------------|----------|--------------|
| `BOT_TOKEN` | Токен Telegram бота | ✅ |
| `ADMIN_IDS` | ID администраторов | ✅ |
| `DATABASE_URL` | URL базы данных | ❌ |
| `PARSER_INTERVAL` | Интервал парсинга (сек) | ❌ |
| `LOG_LEVEL` | Уровень логирования | ❌ |

## 📊 Источники серверов

### GitHub репозитории
- [barry-far/V2ray-Configs](https://github.com/barry-far/V2ray-Configs)
- [mahdibland/V2RayAggregator](https://github.com/mahdibland/V2RayAggregator)
- [mfuu/v2ray](https://github.com/mfuu/v2ray)
- [peasoft/NoMoreWalls](https://github.com/peasoft/NoMoreWalls)
- И другие...

### Веб-сайты
- VPNGate
- FreeVPN724
- И другие...

## 🛠️ Разработка

### Добавление нового протокола

1. Откройте `config/protocols.py`
2. Добавьте протокол в словарь `PROTOCOLS`:

```python
"new_protocol": {
    "name": "New Protocol",
    "emoji": "🆕",
    "category": "mainstream",
    "description": "Описание протокола",
    "platforms": ["Windows", "macOS", "Linux"],
    "config_format": "custom"
}
```

### Добавление нового парсера

1. Создайте файл в `parsers/`
2. Унаследуйтесь от `BaseParser`
3. Реализуйте метод `parse()`

```python
from parsers.base_parser import BaseParser

class CustomParser(BaseParser):
    async def parse(self):
        # Ваша логика парсинга
        return configs
```

## ☁️ Деплой на Render.com

Подробная инструкция: [DEPLOYMENT.md](DEPLOYMENT.md)

**Быстрый деплой:**

1. Fork этот репозиторий
2. Перейдите на https://dashboard.render.com/blueprints
3. Создайте новый Blueprint Instance
4. Подключите ваш форк
5. Укажите переменные `BOT_TOKEN` и `ADMIN_IDS`
6. Нажмите Apply

Render автоматически создаст:
- ✅ Web Service (API + Bot)
- ✅ PostgreSQL Database
- ✅ HTTPS сертификат

## 🐳 Docker

### Сборка образа

```bash
docker build -t sendvpn .
```

### Запуск контейнера

```bash
docker run -d --name sendvpn \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -p 8000:8000 \
  sendvpn
```

### Docker Compose

```bash
docker-compose up -d
```

## 📱 Инструкции по настройке

### iOS
1. Установите приложение для вашего протокола
2. Скопируйте конфигурацию из бота
3. Импортируйте конфигурацию в приложение

### Android
1. Установите приложение для вашего протокола
2. Отсканируйте QR-код или скопируйте конфигурацию
3. Подключитесь к серверу

### Windows / macOS / Linux
Подробные инструкции доступны в боте: `/instructions`

## 💝 Поддержать проект

Проект полностью бесплатный и существует благодаря донатам!

- 💳 **Карта:** `2200 0000 0000 0000`
- ₿ **Bitcoin:** `bc1qxxxxxxxxxxxxxxxxxxxxxx`
- 🔷 **USDT (TRC20):** `TXxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- 💙 **TON:** `UQxxxxxxxxxxxxxxxxxxxxxxxxxx`

## 📄 Лицензия

MIT License - see [LICENSE](LICENSE)

## 🤝 Вклад в проект

Мы приветствуем любой вклад!

1. Fork проекта
2. Создайте ветку (`git checkout -b feature/amazing`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing`)
5. Откройте Pull Request

## 📡 REST API

Полная документация API: [API Docs](https://sendvpn-api.onrender.com/api/docs)

### Основные endpoints:

```bash
# Получить все категории
GET /api/categories

# Получить протоколы
GET /api/protocols?category=v2ray

# Получить серверы
GET /api/servers?protocol=vmess&limit=10

# Случайный сервер
GET /api/servers/random?protocol=vless

# Статистика
GET /api/stats

# Список стран
GET /api/countries
```

## 📞 Контакты

- **API:** https://sendvpn-api.onrender.com/
- **Telegram бот:** [@sendvpn_bot](https://t.me/sendvpn_bot)
- **Разработчик:** [@Xsiwo](https://t.me/Xsiwo)
- **GitHub:** [github.com/Xsiwo/SendVPN](https://github.com/Xsiwo/SendVPN)

## ⚠️ Disclaimer

Этот проект предназначен исключительно для образовательных целей. Использование VPN может быть ограничено в некоторых странах. Убедитесь, что использование VPN законно в вашей юрисдикции.

---

<div align="center">

**Сделано с ❤️ для свободного интернета**

⭐ Поставьте звезду, если проект вам помог!

</div>
