import datetime
import asyncio
from aiogram.enums import ParseMode
from aiogram import Bot
from aiogram.utils import markdown
from aiogram.utils.markdown import hbold, hide_link
from bot.Keyboards.inlineKeyboard import get_link_to_new
from parser import check_updated_news
from bot.db.database import get_subscribed_users
import logging


# utils.py
async def send_news(bot: Bot, chat_id: int, news_list):
    """Отправляет список новостей указанному пользователю."""
    for news_item in news_list:
        news = markdown.text(
            f"{hbold(datetime.datetime.fromtimestamp(news_item['time']))}\n",
            f"{hbold(news_item['title'])}\n",
            f"{hide_link(news_item['img'])}",
            sep="\n",
        )
        await bot.send_message(
            chat_id=chat_id,
            text=news,
            parse_mode=ParseMode.HTML,
            reply_markup=get_link_to_new(news_item["link"]),
        )


async def send_news_to_users(bot: Bot):
    """Рассылает новости всем подписанным пользователям"""
    while True:
        try:
            fresh_news = check_updated_news()
            if fresh_news:
                subscribed_users = get_subscribed_users()
                for user_id in subscribed_users:
                    try:
                        await send_news(bot, user_id, fresh_news)
                    except Exception as e:
                        logging.error(f"Ошибка отправки пользователю {user_id}: {e}")

            await asyncio.sleep(6 * 3600)
        except Exception as e:
            logging.error(f"Ошибка в фоновой задаче: {e}")
            await asyncio.sleep(60)  # Пауза перед повторной попыткой
