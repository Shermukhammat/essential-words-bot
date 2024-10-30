from aiogram import executor, Dispatcher
from loader import dp, bot, db
import handlers
import logging


async def on_start(dp : Dispatcher):
    db.init_bot_info(await bot.get_me())

    # message_data = await bot.send_audio(chat_id='@audiotd', 
    #                      audio=open('data/media/book1/angry_1392933884419.mp3', 'rb'),
    #                      caption="blah")
    # print(message_data)

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    executor.start_polling(dp, skip_updates = False, on_startup = on_start)