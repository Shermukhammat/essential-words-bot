from data import DataBase
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage




db = DataBase('data/data.db')
storage = MemoryStorage()
bot = Bot(db.TOKEN)
dp = Dispatcher(bot, storage=storage)