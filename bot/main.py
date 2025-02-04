import logging
import sys
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import settings
from routers import router as main_router
from utils import send_news_to_users

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
    print(f"Bot token: {settings.bot_token}")  # Отладочный вывод
    asyncio.run(main())