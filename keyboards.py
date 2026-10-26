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
                text="🥗 Основной продукт (Меню на неделю)",
                callback_data="menu:product"
            )
        ],
        [
            InlineKeyboardButton(
                text="⭐️ Отзывы и фото блюд подписчиц",
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
    """Клавиатура раздела Лид-магнита"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📖 Экспресс-рецепты в боте",
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
    """Клавиатура основного продукта с кнопками оплаты"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="💳 Оплатить через Tribute (Telegram)",
                url=config.PAYMENT_TRIBUTE_URL
            )
        ],
        [
            InlineKeyboardButton(
                text="💳 Оплатить через Lava (Карты РФ / Мир)",
                url=config.PAYMENT_LAVA_URL
            )
        ],
        [
            InlineKeyboardButton(
                text="❓ Вопрос по меню / оплате",
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
                text="📸 Канал с отзывами и фото блюд",
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
