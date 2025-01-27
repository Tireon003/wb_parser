from aiogram import Bot, Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware
import asyncio
import logging

from config import settings
from src.handlers import common_router


def init_logging() -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
    )


async def start_bot() -> None:
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.message.middleware(ChatActionMiddleware())

    dp.include_router(common_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main() -> None:
    init_logging()
    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())
