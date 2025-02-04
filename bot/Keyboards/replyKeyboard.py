from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class ButtonText:
    NEWS_BTN = "Получить новости за 5 дней"
    FRESH_NEWS_BTN = "Обновить новости"
    LAST_FIVE_BTN = "Последние 5 новостей"
    HELP = "Помощь"
    SUBSCRIBE = "Рассылка"


def get_on_start_kb():
    news_button = KeyboardButton(text=ButtonText.NEWS_BTN)
    fresh_news_button = KeyboardButton(text=ButtonText.FRESH_NEWS_BTN)
    last_five_button = KeyboardButton(text=ButtonText.LAST_FIVE_BTN)
    help_button = KeyboardButton(text=ButtonText.HELP)
    subscribe_button = KeyboardButton(text=ButtonText.SUBSCRIBE)
    first_row = [news_button, fresh_news_button]
    second_row = [last_five_button, help_button]
    third_row = [subscribe_button]
    markup = ReplyKeyboardMarkup(
        keyboard=[first_row, second_row, third_row],
        resize_keyboard=True,
    )

    return markup
