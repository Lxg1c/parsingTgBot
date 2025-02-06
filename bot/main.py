import logging
import sys
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.config import settings
from bot.routers import router as main_router
from bot.utils.utils import send_news_to_users

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(
        settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(main_router)

    # Запускаем фоновую задачу
    asyncio.create_task(send_news_to_users(bot))

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())