"""
Обработчики callback запросов
"""
import random
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from database import AsyncSessionLocal, Server
from config.protocols import PROTOCOLS, CATEGORIES, get_protocol_by_category
from bot.keyboards import (
    get_categories_keyboard,
    get_protocol_keyboard,
    get_servers_keyboard,
    get_server_details_keyboard,
    get_instructions_keyboard
)
from utils.server_manager import ServerManager

router = Router()


@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery):
    """Возврат к категориям"""
    text = """
🌟 <b>Выберите категорию протоколов:</b>

Выберите нужную категорию, чтобы увидеть доступные протоколы.
"""
    await callback.message.edit_text(
        text,
        reply_markup=get_categories_keyboard(),
        parse_mode='HTML'
    )
    await callback.answer()


@router.callback_query(F.data.startswith("category:"))
async def show_category(callback: CallbackQuery):
    """Показать протоколы категории"""
    category = callback.data.split(":")[1]
    cat_info = CATEGORIES.get(category)

    if not cat_info:
        await callback.answer("❌ Категория не найдена", show_alert=True)
        return

    protocols = get_protocol_by_category(category)

    text = f"""
{cat_info['name']}

<i>{cat_info['description']}</i>

📊 Доступно протоколов: <b>{len(protocols)}</b>

<i>Выберите протокол:</i>
"""

    await callback.message.edit_text(
        text,
        reply_markup=get_protocol_keyboard(category),
        parse_mode='HTML'
    )
    await callback.answer()


@router.callback_query(F.data.startswith("protocol:"))
async def show_protocol(callback: CallbackQuery):
    """Показать информацию о протоколе"""
    protocol_key = callback.data.split(":")[1]
    protocol_info = PROTOCOLS.get(protocol_key)

    if not protocol_info:
        await callback.answer("❌ Протокол не найден", show_alert=True)
        return

    # Получаем количество доступных серверов
    async with AsyncSessionLocal() as session:
        count = await session.scalar(
            select(Server).where(
                Server.protocol == protocol_key,
                Server.is_active == True
            ).count()
        )

    text = f"""
{protocol_info['emoji']} <b>{protocol_info['name']}</b>

📝 {protocol_info['description']}

💻 <b>Платформы:</b>
{', '.join(protocol_info['platforms'])}

🌐 <b>Доступно серверов:</b> {count or 0}

<i>Выберите действие:</i>
"""

    await callback.message.edit_text(
        text,
        reply_markup=get_servers_keyboard(protocol_key),
        parse_mode='HTML'
    )
    await callback.answer()


@router.callback_query(F.data.startswith("random_server:"))
async def get_random_server(callback: CallbackQuery):
    """Получить случайный сервер"""
    protocol = callback.data.split(":")[1]

    async with AsyncSessionLocal() as session:
        # Получаем случайный активный сервер
        servers = await session.execute(
            select(Server).where(
                Server.protocol == protocol,
                Server.is_active == True
            )
        )
        servers_list = servers.scalars().all()

        if not servers_list:
            await callback.answer(
                "😔 Серверы для этого протокола временно недоступны. Попробуйте позже.",
                show_alert=True
            )
            return

        server = random.choice(servers_list)

        protocol_info = PROTOCOLS.get(protocol, {})
        text = f"""
{protocol_info.get('emoji', '🌐')} <b>{protocol_info.get('name', protocol)}</b>

🌍 <b>Страна:</b> {server.country or 'Не указана'}
📍 <b>Город:</b> {server.city or 'Не указан'}
🔌 <b>IP:</b> <code>{server.ip_address or 'N/A'}</code>
🔢 <b>Порт:</b> <code>{server.port or 'N/A'}</code>

⚡ <b>Скорость:</b> {f"{server.speed_mbps} Mbps" if server.speed_mbps else 'Не измерена'}
📡 <b>Пинг:</b> {f"{server.ping_ms} ms" if server.ping_ms else 'Не измерен'}

📋 <b>Конфигурация:</b>
<code>{server.config_data}</code>

<i>Скопируйте конфигурацию и импортируйте в ваш VPN клиент</i>
"""

        await callback.message.edit_text(
            text,
            reply_markup=get_server_details_keyboard(server.id, protocol),
            parse_mode='HTML'
        )
        await callback.answer("✅ Сервер получен!")


@router.callback_query(F.data == "stats")
async def show_stats(callback: CallbackQuery):
    """Показать статистику"""
    async with AsyncSessionLocal() as session:
        from sqlalchemy import func
        from database import User

        total_users = await session.scalar(select(func.count(User.id)))
        total_servers = await session.scalar(select(func.count(Server.id)))
        active_servers = await session.scalar(
            select(func.count(Server.id)).where(Server.is_active == True)
        )

    text = f"""
📊 <b>Статистика SendVPN</b>

👥 Пользователей: <code>{total_users or 0}</code>
🌐 Всего серверов: <code>{total_servers or 0}</code>
✅ Активных серверов: <code>{active_servers or 0}</code>
🔧 Протоколов: <code>{len(PROTOCOLS)}</code>
📂 Категорий: <code>{len(CATEGORIES)}</code>

<i>Обновляется каждый час</i>
"""

    await callback.answer()
    await callback.message.answer(text, parse_mode='HTML')


@router.callback_query(F.data == "help")
async def show_help(callback: CallbackQuery):
    """Показать помощь"""
    help_text = """
📖 <b>Помощь по боту SendVPN</b>

<b>Как пользоваться:</b>
1️⃣ Выберите категорию протоколов
2️⃣ Выберите конкретный протокол
3️⃣ Получите конфигурацию сервера
4️⃣ Импортируйте в ваш VPN клиент

<b>Нужна помощь с настройкой?</b>
Используйте команду /instructions

<b>Поддержка:</b> @sendvpn_support
"""

    await callback.answer()
    await callback.message.answer(help_text, parse_mode='HTML')


@router.message(F.text == "🌟 Выбрать VPN")
async def choose_vpn(message: Message):
    """Выбор VPN"""
    text = """
🌟 <b>Выберите категорию протоколов:</b>

Выберите нужную категорию, чтобы увидеть доступные протоколы.
"""
    await message.answer(
        text,
        reply_markup=get_categories_keyboard(),
        parse_mode='HTML'
    )


@router.message(F.text == "📊 Статистика")
async def show_stats_button(message: Message):
    """Показать статистику по кнопке"""
    async with AsyncSessionLocal() as session:
        from sqlalchemy import func
        from database import User

        total_users = await session.scalar(select(func.count(User.id)))
        total_servers = await session.scalar(select(func.count(Server.id)))
        active_servers = await session.scalar(
            select(func.count(Server.id)).where(Server.is_active == True)
        )

    text = f"""
📊 <b>Статистика SendVPN</b>

👥 Пользователей: <code>{total_users or 0}</code>
🌐 Всего серверов: <code>{total_servers or 0}</code>
✅ Активных серверов: <code>{active_servers or 0}</code>
🔧 Протоколов: <code>{len(PROTOCOLS)}</code>
📂 Категорий: <code>{len(CATEGORIES)}</code>

<i>Обновляется каждый час</i>
"""

    await message.answer(text, parse_mode='HTML')


@router.message(F.text == "📱 Инструкции")
async def show_instructions_button(message: Message):
    """Показать инструкции"""
    text = """
📱 <b>Инструкции по настройке</b>

Выберите вашу платформу:
"""
    await message.answer(
        text,
        reply_markup=get_instructions_keyboard(),
        parse_mode='HTML'
    )


@router.message(F.text == "💝 Поддержать проект")
async def show_donate_button(message: Message):
    """Показать информацию о донатах"""
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
