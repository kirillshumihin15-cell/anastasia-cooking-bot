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
    Поддерживает как текстовые сообщения, так и сообщения с фото/подписью.
    """
    try:
        # Если исходное сообщение с фото
        if message.photo:
            # Если текст укладывается в лимит подписи Telegram (1024 символа)
            if len(text) <= 1024:
                try:
                    return await message.edit_caption(
                        caption=text,
                        reply_markup=reply_markup,
                        parse_mode=parse_mode
                    )
                except TelegramBadRequest as e:
                    if "message is not modified" in str(e).lower():
                        return message
                    # При других ошибках переходим к удалению и отправке текста
                    pass
            
            # Если текст длинный (>1024) или edit_caption не сработал: удаляем фото и шлем текст
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
        else:
            # Обычное текстовое сообщение
            return await message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview
            )
    except TelegramBadRequest as e:
        err_msg = str(e).lower()
        if "message is not modified" in err_msg:
            return message
        
        logger.warning(f"Ошибка редактирования: {e}. Удаляем старое и отправляем новое...")
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
        logger.error(f"Непредвиденная ошибка в safe_edit_text: {e}")
        return await message.answer(
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )


async def safe_edit_or_send_photo(
    message: types.Message,
    photo_path: str,
    caption: str,
    reply_markup: types.InlineKeyboardMarkup = None,
    parse_mode: str = "HTML"
) -> types.Message:
    """
    Безопасная смена фото (через edit_media) или отправка нового фото с подписью.
    """
    try:
        if message.photo:
            try:
                media = types.InputMediaPhoto(
                    media=types.FSInputFile(photo_path),
                    caption=caption,
                    parse_mode=parse_mode
                )
                return await message.edit_media(
                    media=media,
                    reply_markup=reply_markup
                )
            except TelegramBadRequest as e:
                if "message is not modified" in str(e).lower():
                    return message
                logger.warning(f"edit_media не прошел ({e}), удаляем старое и отправляем фото...")
        
        # Если было текстовое сообщение или edit_media вызвал ошибку
        try:
            await message.delete()
        except Exception:
            pass
            
        return await message.answer_photo(
            photo=types.FSInputFile(photo_path),
            caption=caption,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    except Exception as e:
        logger.error(f"Непредвиденная ошибка в safe_edit_or_send_photo: {e}")
        try:
            await message.delete()
        except Exception:
            pass
        return await message.answer_photo(
            photo=types.FSInputFile(photo_path),
            caption=caption,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
