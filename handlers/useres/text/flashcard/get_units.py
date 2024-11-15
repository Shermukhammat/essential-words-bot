from loader import dp, db, bot
from utilites.states.useres import UserState
from utilites.buttons import DefoltButton, InlineButtons
from aiogram.dispatcher import FSMContext
from aiogram import types

@dp.message_handler(state=UserState.flashcard.get_units)
async def get_units_text_flashcards(update : types.Message, state : FSMContext):
    state_data = await state.get_data()
    selected = state_data.get('selected', [])
    book = state_data.get("book")

    if selected:
        await update.answer(f"📖 Book {book} flashcard \n❌ Bekor qilish yoki keyingi tugmasni bosing", 
                        reply_markup=InlineButtons.unit_buttons(selected, book = book))

    else:
        await update.answer(f"📖 Book {book} flashcard \n❌ Unitni tanlang yoki bekor qilish tugmasni bosing", 
                        reply_markup=InlineButtons.unit_buttons(selected, book = book))
        