from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from utilites.states.useres import UserState
from utilites.buttons import DefoltButton
import re


books = ["📗", "📕", "📘", "📙", "📔", "📓"]

@dp.message_handler(state=UserState.book_menu)
async def book_menu_handler(update : types.Message, state : FSMContext):
    
    if update.text == "⬅️ Orqaga":
        await state.finish()

        await update.answer("🎛 Bosh menu", reply_markup=DefoltButton.user_home_menu)


    elif re.search(r'Unit\s(30|[1-9]|[12][0-9])\b', update.text):
        state_data = await state.get_data()
        book_num = state_data.get('book', 1)
        unit = int(update.text[-2:])

        await state.update_data(unit = unit)
        await state.set_state(UserState.unit_menu)
        
        await update.answer(f"{books[book_num-1]} Unit {unit} menu", reply_markup=DefoltButton.get_unit_menu(unit = unit, book = book_num))
    
    elif re.search(r'Yuklash', update.text):
        state_data = await state.get_data()
        book_num = state_data.get('book', 1)

        pdf = db.get_book_pdf(book_num)
        audio = db.get_book_audio(book_num)
        appendix = db.get_book_appendix(book_num)

        if pdf:
            await bot.copy_message(chat_id=update.from_user.id,
                                   message_id=pdf,
                                   from_chat_id=db.DATA_CHANEL,
                                   caption=f"[{db.bot.full_name} bot]({db.bot.url})",
                                   parse_mode=types.ParseMode.MARKDOWN)
        
        if audio:
            await bot.copy_message(chat_id=update.from_user.id,
                                   message_id=audio,
                                   from_chat_id=db.DATA_CHANEL,
                                   caption=f"[{db.bot.full_name} bot]({db.bot.url})",
                                   parse_mode=types.ParseMode.MARKDOWN)
        
    elif re.search(r'APPENDIX', update.text):
        state_data = await state.get_data()
        book_num = state_data.get('book', 1)
        appendix = db.get_book_appendix(book_num)

        if not appendix:
            await update.answer("Ushbu kitob uchun appendix mavjud emas", 
                            reply_markup = DefoltButton.get_book_menu(book_num))
            return

        for message_id in appendix:
            await bot.copy_message(chat_id=update.from_user.id,
                                   message_id=message_id,
                                   from_chat_id=db.DATA_CHANEL)

    else:
        state_data = await state.get_data()
        book_num = state_data.get('book', 1)

        await update.answer("❌ Noto'gri buyruq", 
                            reply_markup = DefoltButton.get_book_menu(book_num))