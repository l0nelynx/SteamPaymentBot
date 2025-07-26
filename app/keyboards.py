import os

from aiogram.types import InlineKeyboardButton, WebAppInfo, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def payment_keyboard(amount):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Оплатить {amount} ⭐️", pay=True)
    return builder.as_markup()


steam_button = InlineKeyboardButton(
    text="🎮 Пополнить STEAM",
    web_app=WebAppInfo(url=os.environ["URL_STEAM"])
)
others_button = InlineKeyboardButton(
    text=u"\U0001F3AE"+" Оплата других сервисов (PSN, Xbox...)",
    callback_data='Others')

psnus_button = InlineKeyboardButton(
    text=u"\U0001F1FA"+u"\U0001F1F8"+" PlayStation Network US 10 USD",
    web_app=WebAppInfo(url=os.environ["URL_PSNUS"])
)
nint_button = InlineKeyboardButton(
    text=u"\U0001F1EF"+u"\U0001F1F5"+" Nintendo eShop 10 USD(US)",
    web_app=WebAppInfo(url=os.environ["URL_NINT"])
)
pscard_button = InlineKeyboardButton(
    text=u"\U0001F4B3"+" PlayStation Store Card $10",
    web_app=WebAppInfo(url=os.environ["URL_PSCARD"])
)
xbox_button = InlineKeyboardButton(
    text=u"\U0001F3AE"+" Xbox US 10 USD",
    web_app=WebAppInfo(url=os.environ["URL_XBOX"])
)
to_main_button = InlineKeyboardButton(text='На главную', callback_data='Main')
# Собираем клавиатуру
main = InlineKeyboardMarkup(inline_keyboard=[[steam_button],
                                             [others_button]])

others = InlineKeyboardMarkup(inline_keyboard=[[psnus_button],
                                               [nint_button],
                                               [pscard_button],
                                               [xbox_button],
                                               [to_main_button]])
