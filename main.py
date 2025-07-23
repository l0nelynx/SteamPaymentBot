import logging
import os
from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.types import LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from app.settings import bot
from app.handlers.events import start_bot, stop_bot
from app.utils import check_amount
import app.database.requests as rq
# import subprocess
# Инициализация бота
dp = Dispatcher()

dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)
crypto = os.environ["CRYPTO"]


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    web_app_button = InlineKeyboardButton(
        text="🎮 Пополнить STEAM",
        web_app=WebAppInfo(url=os.environ["URL"])
    )

    # Собираем клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])

    # Отправляем сообщение с кнопкой
    await message.answer(
        "💳 <b>Пополнение кошелька Steam для РФ и СНГ</b>\n"
        "└ Комиссия платежной системы: 2%\n\n"
        "🔄 <b>Потери при конвертации валюты</b>\n"
        "└ До 10% (максимальный порог)\n\n"
        "ℹ️ Бот не берет комиссию с платежей.\n"
        "Поэтому всегда рады Вашей поддержке\n"
        "/donate <i>сумма</i>⭐️\n"
        f"Или crypto: <code>{crypto}</code>",
        reply_markup=keyboard, parse_mode="HTML"
    )


@dp.message(Command("donate"))
async def send_invoice_handler(message: Message, command: CommandObject):
    prices = [LabeledPrice(label="XTR", amount=check_amount(command.args))]
    await message.answer_invoice(
        title="Поддержка канала",
        description=f"Поддержать сервис на {check_amount(command.args)} ⭐️!",
        prices=prices,
        provider_token="",
        payload="channel_support",
        currency="XTR",
        reply_markup=payment_keyboard(check_amount(command.args)),
    )
    logging.info("Запускаю инвойс")


def payment_keyboard(amount):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Оплатить {amount} ⭐️", pay=True)

    return builder.as_markup()


@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    logging.info("Запускаю pre_checkout_handler")
    await pre_checkout_query.answer(ok=True)


@dp.message(F.successful_payment)
async def success_payment_handler(message: Message):

    await message.answer(text="🥳Спасибо за вашу поддержку!🤗")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    dp.run_polling(bot)
