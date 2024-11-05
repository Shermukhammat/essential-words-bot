from loader import db, dp, bot
from data import Unit, BookData, Word
from aiogram import types
from aiogram.dispatcher import FSMContext
from utilites.states.useres import UserState
from utilites.buttons import DefoltButton, InlineButtons
import re


books = ["📗", "📕", "📘", "📙", "📔", "📓"]

@dp.message_handler(state=UserState.unit_menu)
async def unit_menu_handler(update : types.Message, state : FSMContext):
    state_data = await state.get_data()

    unit = state_data.get('unit', 1)
    book = state_data.get('book', 1)

    if update.text == "⬅️ Orqaga":
       await state.set_state(UserState.book_menu)
       await update.answer(f"{books[book-1]} Book {book} menu", reply_markup=DefoltButton.get_book_menu(book))
    
    elif update.text == "🎛 Bosh menu":
        await state.finish()
        await update.answer("🎛 Bosh menu", reply_markup=DefoltButton.user_home_menu)
    
    elif re.search(r'Word list', update.text):
        text = await get_word_list(book, unit)
        if text:
            await update.answer(text, 
                                parse_mode=types.ParseMode.MARKDOWN,
                                reply_markup=InlineButtons.wordlist_buttons(book, unit))        

    elif re.search(r'Exercise', update.text):
        unitt = await db.get_unit(book, unit)
        for photo_id in unitt.exercise:
            await bot.copy_message(chat_id=update.from_user.id,
                                   message_id=photo_id,
                                   from_chat_id=db.DATA_CHANEL)
    
    elif re.search(r'Reading', update.text):
        unitt = await db.get_unit(book, unit)
        for photo_id in unitt.reading_photos:
            await bot.copy_message(chat_id=update.from_user.id,
                                   message_id=photo_id,
                                   from_chat_id=db.DATA_CHANEL)
            
        if unitt.reading_audio:
            await bot.copy_message(chat_id=update.from_user.id,
                                   message_id=unitt.reading_audio,
                                   from_chat_id=db.DATA_CHANEL)

    else:
        await update.answer("❌ Noto'gri buyruq", 
                            reply_markup = DefoltButton.get_unit_menu(unit = unit, book = book))



async def get_word_list(book : int, unit_num : int) -> str:
    unit = await db.get_unit(book, unit_num)
    if unit:
        return unit.text