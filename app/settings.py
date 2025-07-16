from dataclasses import dataclass

from aiogram import Bot

@dataclass
class Secrets:
    token: str = os.environ["TOKEN"]
    admin_id: int = os.environ["ADMIN_ID"]
    
bot = Bot(token=Secrets.token)
