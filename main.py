import logging
from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram.types import LabeledPrice, PreCheckoutQuery
from app.settings import bot
from app.handlers.events import start_bot, stop_bot, userlist
from app.utils import check_amount
from app.handlers.events import main_menu, main_call
import app.database.requests as rq
from app.keyboards import payment_keyboard
import app.keyboards as kb
from app.settings import Secrets
# import subprocess
# Инициализация бота
dp = Dispatcher()

dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await main_menu(message)
    # Отправляем сообщение с кнопкой


@dp.message(Command("users"), F.from_user.id == Secrets.admin_id)
async def user_db_check(message: Message):
    await userlist()


@dp.callback_query(F.data == 'Main')
async def others(callback: CallbackQuery):
    await callback.answer('Вы в главном меню')
    await main_call(callback)


@dp.callback_query(F.data == 'Others')
async def others(callback: CallbackQuery):
    await callback.answer('Вы выбрали оплату других сервисов')
    await callback.message.answer('На данный момент доступны следующие услуги:', reply_markup=kb.others)


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
