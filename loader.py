from data import DataBase, BookData
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage




db = DataBase('data/data.db')
storage = MemoryStorage()
bot = Bot(db.TOKEN)
dp = Dispatcher(bot, storage=storage)


books_data = {num : BookData(f'data/book{num}.yaml') for num in range(1, 7)}