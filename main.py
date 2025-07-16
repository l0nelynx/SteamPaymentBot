import logging,os
from aiogram import Dispatcher, types
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from botlogic.settings import bot
from botlogic.handlers.events import start_bot, stop_bot

# Инициализация бота
#bot = Bot(token=tkn_bot)
dp = Dispatcher()

@dp.startup.register(start_bot)
@dp.shutdown.register(stop_bot)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🌟 Добро пожаловать в бота для поддержки!\n"
        "Используйте команду /donate чтобы отправить Telegram Stars разработчику."
    )
@dp.message(Command("donate"))
async def send_invoice_handler(message: Message):
    prices = [LabeledPrice(label="XTR", amount=20)]
    await message.answer_invoice(
        title="Поддержка канала",
        description="Поддержать канал на 20 звёзд!",
        prices=prices,
        provider_token="",
        payload="channel_support",
        currency="XTR",
        reply_markup=payment_keyboard(),
    )
def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Оплатить 20 ⭐️", pay=True)

    return builder.as_markup()

from aiogram.types import PreCheckoutQuery


async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


async def success_payment_handler(message: Message):
    await message.answer(text="🥳Спасибо за вашу поддержку!🤗")



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    dp.run_polling(bot)
