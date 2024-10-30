from loader import dp, bot
from aiogram import types
from asyncio import sleep


@dp.channel_post_handler(regexp=r'/id')
async def chanel_post(update : types.Message):
    id = update.sender_chat.id
    data = await update.answer(f"id: `{id}`", parse_mode=types.ParseMode.MARKDOWN)

    await sleep(5)
    try:
        await update.delete()
        await bot.delete_message(chat_id=id, message_id=data.message_id)
    except:
        pass
    
    