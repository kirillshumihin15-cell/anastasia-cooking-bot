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
                text="💬 Поддержка и связь",
                callback_data="menu:contact"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_recipes_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура раздела ТОП-5 рецептов для похудения"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🍗 1. Курочка в соусе с черри (~148 ₽)",
                callback_data="recipe:item_1"
            )
        ],
        [
            InlineKeyboardButton(
                text="🥑 2. Хрустящие баклажаны (~160 ₽)",
                callback_data="recipe:item_2"
            )
        ],
        [
            InlineKeyboardButton(
                text="🍝 3. ПП-паста с индейкой (~153 ₽)",
                callback_data="recipe:item_3"
            )
        ],
        [
            InlineKeyboardButton(
                text="🐟 4. Боул с тунцом и яйцом (~171 ₽)",
                callback_data="recipe:item_4"
            )
        ],
        [
            InlineKeyboardButton(
                text="🥞 5. ПП-сырники без муки (~119 ₽)",
                callback_data="recipe:item_5"
            )
        ],
        [
            InlineKeyboardButton(
                text="📖 Читать все 5 рецептов разом",
                callback_data="recipe:all"
            )
        ]
    ]
    
    if config.LEAD_MAGNET_URL:
        keyboard.append([
            InlineKeyboardButton(
                text="📥 Скачать полный PDF-гайд",
                url=config.LEAD_MAGNET_URL
            )
        ])
        
    keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Назад в главное меню",
            callback_data="menu:main"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_recipe_detail_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура просмотра отдельного рецепта"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Ко всем 5 рецептам",
                    callback_data="menu:recipes"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 В главное меню",
                    callback_data="menu:main"
                )
            ]
        ]
    )


def get_product_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура доступа в закрытый канал: только Tribute и менеджер"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="💳 Оплатить доступ (Tribute)",
                url=config.PAYMENT_TRIBUTE_URL
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Вопрос по каналу (Менеджер)",
                url=config.MANAGER_CONTACT
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
    """Клавиатура связи с менеджером проекта"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="💬 Написать менеджеру (@shymlhln)",
                url=config.MANAGER_CONTACT
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
