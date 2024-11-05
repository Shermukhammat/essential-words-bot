from loader import dp, db, bot
from aiogram import types
from utilites.buttons import InlineButtons
from data import Unit


@dp.callback_query_handler(state="*")
async def query_handler(update : types.CallbackQuery):
    if update.data == 'x':
        await update.answer("❌ Bu tugmadan faqat 1 marta foydalnish mumkun", show_alert=True, cache_time = 30)
        return
    
    unit = await get_unit(update.data)
    if unit:
        await update.message.edit_reply_markup(InlineButtons.wordlist_buttons(unit.book_num, unit.num, forbid_photo = True))

        for id in unit.photos_id:
            await bot.copy_message(chat_id=update.from_user.id,
                                   message_id=id,
                                   from_chat_id=db.DATA_CHANEL)
        


async def get_unit(query : str) -> Unit:
    params = query.split('&')
    if len(params) == 2 and params[0].isnumeric() and params[1].isnumeric():
        book = int(params[0])
        unit = int(params[1])

        if book >= 1 and book <= 6 and unit <= 30 and unit >= 1:
            # return books_data[book].units[unit], book, unit
            return await db.get_unit(book, unit)