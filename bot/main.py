"""
Главный Telegram бот SendVPN
"""
import os
import sys
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

# Импорты из проекта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database import init_db, AsyncSessionLocal, User
from config.protocols import PROTOCOLS, CATEGORIES, get_protocol_by_category, get_all_categories
from bot.keyboards import get_main_keyboard, get_categories_keyboard, get_protocol_keyboard, get_back_keyboard
from bot.handlers import router
from utils.server_manager import ServerManager

# Загрузка переменных окружения
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env файле!")

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем роутер с хендлерами
dp.include_router(router)


class BotStates(StatesGroup):
    """Состояния бота"""
    main_menu = State()
    browsing_categories = State()
    browsing_protocols = State()
    viewing_servers = State()


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Команда /start"""
    # Сохраняем пользователя в БД
    async with AsyncSessionLocal() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                language_code=message.from_user.language_code or 'ru'
            )
            session.add(user)
            await session.commit()

    await state.set_state(BotStates.main_menu)

    welcome_text = f"""
👋 <b>Привет, {message.from_user.first_name}!</b>

Добро пожаловать в <b>SendVPN</b> — крупнейший агрегатор бесплатных VPN серверов!

🌍 <b>У нас доступны:</b>
• {len(PROTOCOLS)} протоколов
• {len(CATEGORIES)} категорий
• Тысячи серверов по всему миру

🆓 <b>Всё полностью бесплатно!</b>
Поддержите проект донатом, если хотите 💝

<i>Выберите категорию протоколов ниже:</i>
"""

    await message.answer(
        welcome_text,
        reply_markup=get_categories_keyboard(),
        parse_mode='HTML'
    )


@dp.message(Command('help'))
async def cmd_help(message: Message):
    """Команда /help"""
    help_text = """
📖 <b>Помощь по боту SendVPN</b>

<b>Команды:</b>
/start - Главное меню
/help - Эта справка
/stats - Статистика проекта
/donate - Поддержать проект

<b>Как пользоваться:</b>
1️⃣ Выберите категорию протоколов
2️⃣ Выберите конкретный протокол
3️⃣ Получите конфигурацию сервера
4️⃣ Импортируйте в ваш VPN клиент

<b>Нужна помощь с настройкой?</b>
Нажмите на кнопку "📱 Инструкции" в главном меню!

<b>Поддержка:</b> @sendvpn_support
"""
    await message.answer(help_text, parse_mode='HTML')


@dp.message(Command('stats'))
async def cmd_stats(message: Message):
    """Команда /stats"""
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select, func
        from database import User, Server

        # Считаем статистику
        total_users = await session.scalar(select(func.count(User.id)))
        total_servers = await session.scalar(select(func.count(Server.id)))
        active_servers = await session.scalar(
            select(func.count(Server.id)).where(Server.is_active == True)
        )

    stats_text = f"""
📊 <b>Статистика SendVPN</b>

👥 Пользователей: <code>{total_users or 0}</code>
🌐 Всего серверов: <code>{total_servers or 0}</code>
✅ Активных серверов: <code>{active_servers or 0}</code>
🔧 Протоколов: <code>{len(PROTOCOLS)}</code>
📂 Категорий: <code>{len(CATEGORIES)}</code>

<i>Обновляется каждый час</i>
"""
    await message.answer(stats_text, parse_mode='HTML')


@dp.message(Command('donate'))
async def cmd_donate(message: Message):
    """Команда /donate"""
    donate_text = """
💝 <b>Поддержать проект</b>

Проект SendVPN полностью бесплатный и существует благодаря вашим донатам!

<b>Способы поддержки:</b>

💳 <b>Карта:</b>
<code>2200 0000 0000 0000</code>

₿ <b>Bitcoin:</b>
<code>bc1qxxxxxxxxxxxxxxxxxxxxxx</code>

🔷 <b>USDT (TRC20):</b>
<code>TXxxxxxxxxxxxxxxxxxxxxxxxxxxx</code>

💙 <b>TON:</b>
<code>UQxxxxxxxxxxxxxxxxxxxxxxxxxx</code>

Спасибо за вашу поддержку! ❤️
"""
    await message.answer(donate_text, parse_mode='HTML')


async def main():
    """Запуск бота"""
    print("🚀 Запуск SendVPN бота...")

    # Инициализация БД
    await init_db()
    print("✅ База данных инициализирована")

    # Запуск парсеров в фоне (опционально)
    # asyncio.create_task(run_parsers())

    # Запуск бота
    print("✅ Бот запущен!")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")
