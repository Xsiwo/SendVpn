"""
Клавиатуры для Telegram бота
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config.protocols import CATEGORIES, get_protocol_by_category


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главная клавиатура"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌟 Выбрать VPN")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="📱 Инструкции")],
            [KeyboardButton(text="💝 Поддержать проект")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_categories_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с категориями протоколов"""
    builder = InlineKeyboardBuilder()

    for cat_key, cat_data in CATEGORIES.items():
        protocols_count = len(get_protocol_by_category(cat_key))
        button_text = f"{cat_data['name']} ({protocols_count})"
        builder.button(
            text=button_text,
            callback_data=f"category:{cat_key}"
        )

    # По 1 кнопке в ряд для красоты
    builder.adjust(1)

    # Кнопки внизу
    builder.row(
        InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
        InlineKeyboardButton(text="❓ Помощь", callback_data="help")
    )

    return builder.as_markup()


def get_protocol_keyboard(category: str) -> InlineKeyboardMarkup:
    """Клавиатура с протоколами категории"""
    builder = InlineKeyboardBuilder()

    protocols = get_protocol_by_category(category)
    for protocol in protocols:
        button_text = f"{protocol['emoji']} {protocol['name']}"
        builder.button(
            text=button_text,
            callback_data=f"protocol:{protocol['key']}"
        )

    # По 2 кнопки в ряд
    builder.adjust(2)

    # Кнопка "Назад"
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_categories")
    )

    return builder.as_markup()


def get_servers_keyboard(protocol: str, page: int = 0) -> InlineKeyboardMarkup:
    """Клавиатура для списка серверов"""
    builder = InlineKeyboardBuilder()

    # Кнопки получения сервера
    builder.row(
        InlineKeyboardButton(text="🎲 Случайный сервер", callback_data=f"random_server:{protocol}"),
        InlineKeyboardButton(text="📋 Список серверов", callback_data=f"list_servers:{protocol}:0")
    )

    # Пагинация (если нужно)
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"list_servers:{protocol}:{page-1}"))
    nav_buttons.append(InlineKeyboardButton(text="🔄 Обновить", callback_data=f"refresh_servers:{protocol}"))
    if True:  # Проверка есть ли еще серверы
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"list_servers:{protocol}:{page+1}"))

    builder.row(*nav_buttons)

    # Кнопка "Назад"
    builder.row(
        InlineKeyboardButton(text="⬅️ К протоколам", callback_data=f"back_to_protocols")
    )

    return builder.as_markup()


def get_server_details_keyboard(server_id: int, protocol: str) -> InlineKeyboardMarkup:
    """Клавиатура для деталей сервера"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="📋 Копировать конфиг", callback_data=f"copy_config:{server_id}"),
        InlineKeyboardButton(text="📱 QR код", callback_data=f"qr_code:{server_id}")
    )

    builder.row(
        InlineKeyboardButton(text="🎲 Другой сервер", callback_data=f"random_server:{protocol}"),
        InlineKeyboardButton(text="⬅️ К списку", callback_data=f"list_servers:{protocol}:0")
    )

    return builder.as_markup()


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Простая клавиатура с кнопкой Назад"""
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data="back_to_categories")
    return builder.as_markup()


def get_instructions_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для инструкций"""
    builder = InlineKeyboardBuilder()

    platforms = [
        ("📱 iOS", "instructions:ios"),
        ("🤖 Android", "instructions:android"),
        ("🪟 Windows", "instructions:windows"),
        ("🍎 macOS", "instructions:macos"),
        ("🐧 Linux", "instructions:linux")
    ]

    for text, callback in platforms:
        builder.button(text=text, callback_data=callback)

    builder.adjust(2)

    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")
    )

    return builder.as_markup()
