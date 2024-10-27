from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from utilites.states.useres import UserState
from utilites.buttons import DefoltButton
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


    else:
        # await bot.send_poll(
        # chat_id=update.from_user.id,
        # question="What's your favorite color?",
        # options=["Red", "Blue", "Green"],
        # type="quiz",
        # correct_option_id=1,
        # close_date=int((datetime.now() + timedelta(seconds=30)).timestamp()),
        # is_anonymous=False)
    
        await update.answer("🎛 Bosh menu", reply_markup=DefoltButton.user_home_menu)

# @dp.message_handler()
# async def start_registr_handler(update : types.Message, state : FSMContext):
#     # await db.register_user(update.from_user.id, name=update.from_user.first_name)
#     await update.answer(f"Assalomu alaykum [{update.from_user.first_name}]({update.from_user.url}) \n🤖 Men [{db.bot.first_name}]({db.bot.url}) bot man. \n\n👇 O'zingizga kerakli menuyuni tanlang",
#                         parse_mode=types.ParseMode.MARKDOWN,
#                         reply_markup=DefoltButton.user_home_menu)