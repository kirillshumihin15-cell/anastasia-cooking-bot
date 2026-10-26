import logging
from aiogram import types
from aiogram.exceptions import TelegramBadRequest

logger = logging.getLogger(__name__)


async def safe_edit_text(
    message: types.Message,
    text: str,
    reply_markup: types.InlineKeyboardMarkup = None,
    parse_mode: str = "HTML",
    disable_web_page_preview: bool = True
) -> types.Message:
    """
    Безопасное редактирование сообщения для бесшовной инлайн-навигации.
    Предотвращает падение при ошибке 'message is not modified' 
    или если исходное сообщение не может быть отредактировано.
    """
    try:
        return await message.edit_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )
    except TelegramBadRequest as e:
        err_msg = str(e).lower()
        if "message is not modified" in err_msg:
            # Текст и клавиатура не изменились, игнорируем ошибку
            return message
        
        logger.warning(f"Не удалось отредактировать сообщение: {e}. Отправка нового сообщения...")
        # Если редактирование невозможно (например, было медиа-сообщение или удалено)
        try:
            await message.delete()
        except Exception:
            pass
            
        return await message.answer(
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при safe_edit_text: {e}")
        return await message.answer(
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )
