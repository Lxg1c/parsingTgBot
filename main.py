import logging
import sys
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import settings
from routers import router as main_router
from routers.commands.base_commands import on_startup


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(
        settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(main_router)

    # Запускаем фоновую задачу
    await on_startup(bot)

    # And run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())  # Используем asyncio.run для запуска асинхронной функции
