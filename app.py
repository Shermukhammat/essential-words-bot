from aiogram import executor, Dispatcher
from loader import dp, bot, db
import handlers
import logging


async def on_start(dp : Dispatcher):
    db.init_bot_info(await bot.get_me())


if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    executor.start_polling(dp, skip_updates = False, on_startup = on_start)