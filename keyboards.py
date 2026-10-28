from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import config


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура из 4 ключевых разделов"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📖 Топ-рецепты",
                callback_data="menu:recipes"
            )
        ],
        [
            InlineKeyboardButton(
                text="🥗 Закрытый канал (90+ рецептов)",
                callback_data="menu:product"
            )
        ],
        [
            InlineKeyboardButton(
                text="⭐️ Отзывы и результаты",
                callback_data="menu:reviews"
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Связь с Анастасией",
                callback_data="menu:contact"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_recipes_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура раздела Топ-рецептов"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📖 Открыть экспресс-рецепты в боте",
                callback_data="guide:read_online"
            )
        ]
    ]
    
    # Если указана ссылка на скачивание или Telegraph
    if config.LEAD_MAGNET_URL:
        keyboard.append([
            InlineKeyboardButton(
                text="📥 Скачать полный PDF-гайд",
                url=config.LEAD_MAGNET_URL
            )
        ])
        
    keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Назад в меню",
            callback_data="menu:main"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_product_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура доступа в закрытый канал с кнопками оплаты"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="💳 Вступить через Tribute (Telegram)",
                url=config.PAYMENT_TRIBUTE_URL
            )
        ],
        [
            InlineKeyboardButton(
                text="💳 Оплата картой РФ / Мир (Lava)",
                url=config.PAYMENT_LAVA_URL
            )
        ],
        [
            InlineKeyboardButton(
                text="❓ Задать вопрос по доступу",
                url=config.ANASTASIA_CONTACT
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад в меню",
                callback_data="menu:main"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_reviews_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура отзывов с ссылкой на канал"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📸 Смотреть фото блюд и отзывы в канале",
                url=config.REVIEWS_CHANNEL_LINK
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад в меню",
                callback_data="menu:main"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_contact_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура связи с автором"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="💌 Написать Анастасии в ЛС",
                url=config.ANASTASIA_CONTACT
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад в меню",
                callback_data="menu:main"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Универсальная кнопка возврата в меню"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад в меню",
                    callback_data="menu:main"
                )
            ]
        ]
    )
