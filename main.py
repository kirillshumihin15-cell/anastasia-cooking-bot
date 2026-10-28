import asyncio
import logging
import sys
from pathlib import Path
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import config
import database as db
import texts
import keyboards as kb
from utils import safe_edit_text

# Пути к приветственному фото
WELCOME_PHOTO_JPG = Path("assets/welcome.jpg")
WELCOME_PHOTO_PNG = Path("assets/welcome.png")

def get_welcome_photo() -> types.FSInputFile | None:
    """Получить файл фото приветствия (предпочтительно оптимизированный JPG)"""
    if WELCOME_PHOTO_JPG.exists():
        return types.FSInputFile(WELCOME_PHOTO_JPG)
    if WELCOME_PHOTO_PNG.exists():
        return types.FSInputFile(WELCOME_PHOTO_PNG)
    return None

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# ==========================================
# ОБРАБОТЧИКИ ВОРОНКИ И ЗАЯВОК (CHAT JOIN REQUEST)
# ==========================================

@dp.chat_join_request()
async def handle_chat_join_request(event: types.ChatJoinRequest):
    """
    Обработка заявки на вступление в канал (Instagram Reels -> Заявка в канал).
    ВАЖНО: Автоодобрение отключено! Заявки подтверждаются вручную.
    Бот отправляет приветствие с лид-магнитом и меню.
    """
    user = event.from_user
    logger.info(f"Получена заявка в канал от @{user.username} (id: {user.id})")

    # Сохраняем пользователя в БД
    await db.add_or_update_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        source="chat_join_request"
    )

    # Логируем аналитику воронки
    await db.log_event(
        user_id=user.id,
        event_name="chat_join_request_received",
        payload={"chat_id": event.chat.id, "chat_title": event.chat.title}
    )

    await db.set_user_state(
        user_id=user.id,
        state="welcome_sent",
        data={"source": "chat_join_request"}
    )

    # Отправляем фото-приветствие и главное меню
    try:
        photo = get_welcome_photo()
        if photo:
            await bot.send_photo(
                chat_id=user.id,
                photo=photo,
                caption=texts.WELCOME_JOIN_REQUEST,
                reply_markup=kb.get_main_menu_keyboard()
            )
        else:
            await bot.send_message(
                chat_id=user.id,
                text=texts.WELCOME_JOIN_REQUEST,
                reply_markup=kb.get_main_menu_keyboard(),
                disable_web_page_preview=True
            )
    except Exception as e:
        logger.error(f"Не удалось отправить приветствие пользователю {user.id}: {e}")


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    """Прямой запуск бота по команде /start"""
    user = message.from_user
    logger.info(f"Команда /start от @{user.username} (id: {user.id})")

    await db.add_or_update_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        source="direct_start"
    )

    await db.log_event(user_id=user.id, event_name="start_command")
    await db.set_user_state(user_id=user.id, state="main_menu")

    photo = get_welcome_photo()
    if photo:
        await message.answer_photo(
            photo=photo,
            caption=texts.WELCOME_DIRECT,
            reply_markup=kb.get_main_menu_keyboard()
        )
    else:
        await message.answer(
            text=texts.WELCOME_DIRECT,
            reply_markup=kb.get_main_menu_keyboard(),
            disable_web_page_preview=True
        )


@dp.message(Command("stats"))
async def handle_stats(message: types.Message):
    """Статистика для администратора"""
    if config.ADMIN_ID and message.from_user.id != config.ADMIN_ID:
        return

    stats = await db.get_stats()
    events_str = "\n".join([f"• <code>{k}</code>: {v}" for k, v in stats['events'].items()]) or "Пока нет событий"

    text = (
        f"📊 <b>Статистика бота Анастасии:</b>\n\n"
        f"👥 Всего пользователей: <b>{stats['total_users']}</b>\n"
        f"📥 Заявок на вступление: <b>{stats['join_requests']}</b>\n\n"
        f"<b>События воронки:</b>\n{events_str}"
    )
    await message.answer(text=text)


@dp.message(Command("get_pdf"))
async def handle_get_pdf(message: types.Message):
    """Отправка PDF-книги закрытого клуба администратору"""
    if config.ADMIN_ID and message.from_user.id != config.ADMIN_ID:
        return

    pdf_path = Path("assets/База_Рецептов_и_Рационов_Анастасии.pdf")
    if not pdf_path.exists():
        await message.answer("❌ Файл PDF еще не сгенерирован в assets/")
        return

    await message.answer("⏳ Загружаю 43-страничную PDF-книгу закрытого клуба...")
    await message.answer_document(
        document=types.FSInputFile(pdf_path),
        caption=(
            "📖 <b>База Рецептов и Рационов Анастасии (Закрытый Клуб)</b> 🤍\n\n"
            "• 43 страницы премиальной авторской вёрстки\n"
            "• 98 авторских рецептов с КБЖУ, граммовками и ценниками\n"
            "• Система Meal Prep (заготовки на 3 дня за 1 вечер)\n"
            "• 10 народных суперфудов & эликсиров для очищения ЖКТ\n"
            "• Таблица замен продуктов и умный список покупок\n\n"
            "<i>Файл готов для закрепления в приватном канале!</i>"
        )
    )


# ==========================================
# ИНЛАЙН НАВИГАЦИЯ (SAFE EDIT TEXT)
# ==========================================

@dp.callback_query(F.data == "menu:main")
async def nav_main_menu(callback: types.CallbackQuery):
    """Возврат в главное меню"""
    await callback.answer()
    await db.log_event(user_id=callback.from_user.id, event_name="nav_main_menu")
    await db.set_user_state(user_id=callback.from_user.id, state="main_menu")

    await safe_edit_text(
        message=callback.message,
        text=texts.MAIN_MENU,
        reply_markup=kb.get_main_menu_keyboard()
    )


@dp.callback_query(F.data == "menu:recipes")
async def nav_recipes(callback: types.CallbackQuery):
    """Столп 1: Меню ТОП-5 рецептов для похудения"""
    await callback.answer()
    await db.log_event(user_id=callback.from_user.id, event_name="view_top_recipes_menu")
    await db.set_user_state(user_id=callback.from_user.id, state="pillar_recipes")

    await safe_edit_text(
        message=callback.message,
        text=texts.PILLAR_1_RECIPES,
        reply_markup=kb.get_recipes_keyboard()
    )


@dp.callback_query(F.data.startswith("recipe:item_"))
async def nav_recipe_detail(callback: types.CallbackQuery):
    """Просмотр подробной карты конкретного рецепта из 5"""
    await callback.answer()
    recipe_id = int(callback.data.split("_")[1])
    recipe_text = texts.RECIPES_DATA.get(recipe_id, texts.PILLAR_1_RECIPES)

    await db.log_event(
        user_id=callback.from_user.id,
        event_name="view_recipe_detail",
        payload={"recipe_id": recipe_id}
    )

    await safe_edit_text(
        message=callback.message,
        text=recipe_text,
        reply_markup=kb.get_recipe_detail_keyboard()
    )


@dp.callback_query(F.data == "recipe:all")
@dp.callback_query(F.data == "guide:read_online")
async def nav_all_recipes(callback: types.CallbackQuery):
    """Показать все 5 рецептов разом"""
    await callback.answer()
    await db.log_event(user_id=callback.from_user.id, event_name="view_all_recipes")

    await safe_edit_text(
        message=callback.message,
        text=texts.ALL_RECIPES_TEXT,
        reply_markup=kb.get_recipe_detail_keyboard()
    )


@dp.callback_query(F.data == "menu:product")
async def nav_product(callback: types.CallbackQuery):
    """Столп 2: Основной продукт (Меню на неделю / Сборник с оплатой)"""
    await callback.answer()
    await db.log_event(user_id=callback.from_user.id, event_name="view_product")
    await db.set_user_state(user_id=callback.from_user.id, state="pillar_product")

    await safe_edit_text(
        message=callback.message,
        text=texts.PILLAR_2_PRODUCT,
        reply_markup=kb.get_product_keyboard()
    )


@dp.callback_query(F.data == "menu:reviews")
async def nav_reviews(callback: types.CallbackQuery):
    """Столп 3: Отзывы и фото блюд подписчиц"""
    await callback.answer()
    await db.log_event(user_id=callback.from_user.id, event_name="view_reviews")
    await db.set_user_state(user_id=callback.from_user.id, state="pillar_reviews")

    await safe_edit_text(
        message=callback.message,
        text=texts.PILLAR_3_REVIEWS,
        reply_markup=kb.get_reviews_keyboard()
    )


@dp.callback_query(F.data == "menu:contact")
async def nav_contact(callback: types.CallbackQuery):
    """Столп 4: Связь с Анастасией"""
    await callback.answer()
    await db.log_event(user_id=callback.from_user.id, event_name="view_contact")
    await db.set_user_state(user_id=callback.from_user.id, state="pillar_contact")

    await safe_edit_text(
        message=callback.message,
        text=texts.PILLAR_4_CONTACT,
        reply_markup=kb.get_contact_keyboard()
    )


# ==========================================
# HEALTHCHECK СЕРВЕР (ДЛЯ RENDER.COM)
# ==========================================

async def healthcheck_handler(request: web.Request) -> web.Response:
    """Эндпоинт проверки здоровья для Render Web Service"""
    return web.json_response({
        "status": "healthy",
        "service": "anastasia_cooking_bot",
        "uptime": "active"
    })


async def start_healthcheck_server(port: int) -> web.AppRunner:
    """Запуск aiohttp сервера на указанном порту"""
    app = web.Application()
    app.router.add_get("/", healthcheck_handler)
    app.router.add_get("/health", healthcheck_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Healthcheck HTTP-сервер успешно запущен на порту {port}")
    return runner


# ==========================================
# ТОЧКА ВХОДА (MAIN RUNNER)
# ==========================================

async def main():
    if not config.BOT_TOKEN:
        logger.critical("ОШИБКА: BOT_TOKEN не задан в переменных окружения или .env!")
        sys.exit(1)

    # Инициализация SQLite базы данных
    await db.init_db()
    logger.info("База данных SQLite инициализирована.")

    # Запуск aiohttp сервера для Render
    runner = await start_healthcheck_server(config.PORT)

    try:
        logger.info("Бот Анастасии запущен в режиме polling...")
        # Явно указываем обновления, включая chat_join_request
        await dp.start_polling(
            bot,
            allowed_updates=["message", "callback_query", "chat_join_request"]
        )
    finally:
        logger.info("Остановка бота и очистка ресурсов...")
        await runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
