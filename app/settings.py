from dataclasses import dataclass
from aiogram import Bot
import os

@dataclass
class Secrets:
    token: str = os.environ["TOKEN"]
    # admin_id: int = os.environ["ADMIN_ID"]
    # token: str = ''
    admin_id: int = 1058998037
    
bot = Bot(token=Secrets.token)
