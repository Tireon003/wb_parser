from typing import cast
from aiogram import Router, F, types, flags
from aiogram.filters import Command

from src.api import ParserAPI
from src.utils import get_pretty_caption

router = Router()


@router.message(Command("start"))
async def handle_start_message(msg: types.Message) -> None:
    await msg.reply(
        "Привет, я бот для парсинга карточек с WB.\n\n"
        "Что я умею:\n"
        "1. Парсить карточки WB по артикулу\n"
        "2. Сохранять данные карточек в Google-таблицы\n"
        "3. Сохранять текущую таблицу по команде /exp\n"
    )


@router.message(F.text)
@flags.chat_action("typing")
async def handle_article(msg: types.Message) -> None:
    article = msg.text
    article = cast(str, article)

    if not article.isdigit() or 8 > len(article) > 12:
        await msg.reply("Введен некорректный формат артикула!")
        return None

    pending_message = await msg.answer("Запрос обрабатывается...")

    status, content = await ParserAPI.parse_article(int(article))

    if status != 200:
        await pending_message.delete()
        await msg.reply("В процессе парсинга произошла непредвиденная ошибка!")
        return None

    card_data = content["data"]
    card_preview = card_data["pictures"][0]
    caption_text = get_pretty_caption(card_data)

    await pending_message.delete()

    await msg.answer_photo(
        photo=card_preview,
        caption=caption_text,
        reply_markup=types.ReplyKeyboardRemove(),
    )
