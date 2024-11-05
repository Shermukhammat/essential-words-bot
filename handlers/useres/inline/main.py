from loader import dp, db, bot
from aiogram import types
from uuid import uuid4
from data import Unit, Word




@dp.inline_handler(state='*')
async def inline_audio(query: types.InlineQuery):
    unit = await get_unit(query.query)
    if unit:
        answer = [audio(word, num) for num, word in unit.words.items()]

        await bot.answer_inline_query(query.id, results=answer, cache_time=1)


async def get_unit(query : str) -> Unit:
    params = query.split('&')
    if len(params) == 2 and params[0].isnumeric() and params[1].isnumeric():
        book = int(params[0])
        unit = int(params[1])

        if book >= 1 and book <= 6 and unit <= 30 and unit >= 1:
            # return books_data[book].units[unit]
            return await db.get_unit(book, unit)
        
def audio(word: Word, num : int) -> types.InlineQueryResultAudio:
    return types.InlineQueryResultAudio(id=uuid4().hex, 
                                        title=f"{num} {word.value}", 
                                        audio_url=f"https://t.me/{db.DATA_CHANEL_USERNAME}/{word.audio_id}",
                                        caption=f"🔤 {word.value} [{word.type}] {word.translation} \n📖 {word.meanig} \n💡 {word.example} \n\n📖 {word.meanig_tr} \n💡 {word.example_tr}")