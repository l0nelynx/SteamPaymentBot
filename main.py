import logging
from aiogram import Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.settings import bot
from app.handlers.events import start_bot, stop_bot
from aiogram.types import PreCheckoutQuery
import subprocess
# Инициализация бота
# bot = Bot(token=tkn_bot)
dp = Dispatcher()

dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await start_bot()
    await message.answer(
       "🌟 Добро пожаловать в бота для поддержки!\n"
       "Используйте команду /donate чтобы отправить Telegram Stars разработчику."
    )
    try:
        result = subprocess.run(['bash', '-c', 'docker exec target sh -c ./getconf.sh'], capture_output=True, text=True, check=True)
        # docker exec -it sender sh
        # apk add docker-cli  # Установить Docker CLI в контейнер при запуске
        print("Вывод команды:")
        print(result.stdout)
        print("Код возврата:", result.returncode)
    except subprocess.CalledProcessError as e:
        print("Ошибка при выполнении команды:")
        print(e.stderr)
        print("Код возврата:", e.returncode)


@dp.message(Command("donate"))
async def send_invoice_handler(message: Message):
    prices = [LabeledPrice(label="XTR", amount=1)]
    await message.answer_invoice(
        title="Поддержка канала",
        description="Поддержать канал на 1 звёзду!",
        prices=prices,
        provider_token="",
        payload="channel_support",
        currency="XTR",
        reply_markup=payment_keyboard(),
    )
    logging.info("Запускаю инвойс")


def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Оплатить 1 ⭐️", pay=True)

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
