from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from utilites.states.useres import UserState
from utilites.buttons import DefoltButton, InlineButtons
import asyncio, time
from datetime import datetime, timedelta

books = ["📗", "📕", "📘", "📙", "📔", "📓"]


@dp.message_handler(lambda update :  db.is_user(update.from_user.id))
async def main_text_handler(update : types.Message, state : FSMContext):
    if update.text in ["📗 Book 1", "📕 Book 2", "📘 Book 3", "📙 Book 4", "📔 Book 5", "📓 Book 6"]:
        num = int(update.text[-1])

        await state.set_state(UserState.book_menu)
        await state.update_data(book = num)

        await update.answer(f"{books[num-1]} Book {num} menu", reply_markup=DefoltButton.get_book_menu(num))

    elif update.text == "❓ Test":
        await UserState.test.first()
        await update.answer("📝", reply_markup=types.ReplyKeyboardRemove())
        await update.answer("Test uchun kitobni tanlang 👇",
                            reply_markup=InlineButtons.books_button)
        
        await state.update_data(selected = [], random = False, order = 'enuz', time = 30, semaphore = asyncio.Semaphore(1))

    elif update.text == "🀄️ Flashcard":
        await UserState.flashcard.first()

        await update.answer("📝", reply_markup=types.ReplyKeyboardRemove())
        await update.answer("Flashcard uchun kitobni tanlang 👇",
                            reply_markup=InlineButtons.books_button)
        
        await state.update_data(selected = [], random = False, order = 'enuz', time = 30, semaphore = asyncio.Semaphore(1))
    
    elif update.text == "ℹ️ Yordam":
        await update.answer("Ushbu bot sizga `4000 Essential english words` kitobni lug'atni yodlashga yordam beradi.",
                            parse_mode=types.ParseMode.MARKDOWN,
                            reply_markup=DefoltButton.user_home_menu)
    else:
        await update.answer("🎛 Bosh menu", reply_markup=DefoltButton.user_home_menu)

