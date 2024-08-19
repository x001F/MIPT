from aiogram import Bot, Dispatcher
from src.storage import Storage
from src.config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=Storage('src/config/data.db'))
