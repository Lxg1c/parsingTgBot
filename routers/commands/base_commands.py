import json
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils import markdown
from Keyboards.replyKeyboard import get_on_start_kb, ButtonText
from aiogram import F
from parser import check_updated_news
from utils import send_news

router = Router(name=__name__)

# Список для хранения ID пользователей, которым нужно отправлять новости
subscribers = set()


@router.message(CommandStart())
async def handle_start(message: Message):
    subscribers.add(message.from_user.id)  # Добавляем пользователя в подписчики
    await message.answer(
        text=f"Привет, {markdown.hbold(message.from_user.full_name)}!\nЯ бот, который делится "
        f"последними новостями в мире IT. Выберите что хотите, в нижнем меню",
        reply_markup=get_on_start_kb(),
        parse_mode=ParseMode.HTML,
    )


@router.message(F.text == ButtonText.HELP)
@router.message(Command(ButtonText.HELP, prefix="/!%"))
async def get_help(message: Message):
    await message.answer(
        "Я бот, который делится последними новостями в мире IT. Выберите что хотите, в нижнем меню"
    )


@router.message(F.text == ButtonText.LAST_FIVE_BTN)
@router.message(Command(ButtonText.LAST_FIVE_BTN, prefix="/!%"))
@router.message(Command("lastfive", prefix="/!%"))
async def get_last_five_news(message: Message) -> None:
    try:
        with open("news_dict.json", "r", encoding="utf-8") as file:
            news_dict = json.load(file)
    except FileNotFoundError:
        await message.answer("Новости ещё не загружены. Попробуйте позже.")
        return

    # Сортируем новости по времени и берем последние 5
    sorted_news = sorted(news_dict.values(), key=lambda x: x["time"])[-5:]
    await send_news(message, sorted_news)


@router.message(F.text == ButtonText.NEWS_BTN)
@router.message(Command(ButtonText.NEWS_BTN, prefix="/!%"))
@router.message(Command("news", prefix="/!%"))
async def get_all_news(message: Message) -> None:
    try:
        with open("news_dict.json", "r", encoding="utf-8") as file:
            news_dict = json.load(file)
    except FileNotFoundError:
        await message.answer("Новости ещё не загружены. Попробуйте позже.")
        return

    # Сортируем новости по времени
    sorted_news = sorted(news_dict.values(), key=lambda x: x["time"])
    await send_news(message, sorted_news)


@router.message(F.text == ButtonText.FRESH_NEWS_BTN)
@router.message(Command(ButtonText.FRESH_NEWS_BTN, prefix="/!%"))
@router.message(Command("fresh", prefix="/!%"))
async def get_fresh_news(message: Message) -> None:
    # Проверяем обновления и получаем свежие новости
    fresh_news = check_updated_news()

    if not fresh_news:
        await message.answer("Новых новостей пока нет.")
        return

    # Сортируем свежие новости по времени
    sorted_news = sorted(fresh_news.values(), key=lambda x: x["time"], reverse=True)
    await send_news(message, sorted_news)
