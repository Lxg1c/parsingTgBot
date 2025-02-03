from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class LinkBtnText:
    LINK_TEXT = "Подробнее"


def get_link_to_new(link):
    link_btn = InlineKeyboardButton(text=LinkBtnText.LINK_TEXT, url=link)
    markup = InlineKeyboardMarkup(inline_keyboard=[[link_btn]], resize_keyboard=True)

    return markup
