from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils import markdown
from aiogram.utils.markdown import hbold, hide_link
from datetime import datetime
from Keyboards.inlineKeyboard import get_link_to_new


async def send_news(message: Message, news_list):
    """Отправляет список новостей."""
    for news_item in news_list:
        news = markdown.text(
            f"{hbold(datetime.datetime.fromtimestamp(news_item['time']))}\n",
            f"{hbold(news_item['title'])}\n",
            f"{hide_link(news_item['img'])}",
            sep="\n",
        )
        await message.answer(
            news,
            parse_mode=ParseMode.HTML,
            reply_markup=get_link_to_new(news_item["link"]),
        )
