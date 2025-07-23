import asyncio
from app.settings import bot, Secrets
from app.views import start_bot_msg, stop_bot_msg
from app.database.models import async_main


async def start_bot():
    await bot.send_message(Secrets.admin_id, start_bot_msg())
    await async_main() # Создание таблиц БД при запуске


async def stop_bot():
    await bot.send_message(Secrets.admin_id, stop_bot_msg())
