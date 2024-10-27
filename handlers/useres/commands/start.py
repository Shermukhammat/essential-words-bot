from loader import db, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
# from utilites.states.useres import 
from utilites.buttons import DefoltButton


@dp.message_handler(lambda update :  db.is_user(update.from_user.id) ,commands = 'start')
async def start_handler(update : types.Message, state : FSMContext):
    user = await db.get_user(update.from_user.id)

    await update.answer(f"👤 Foydalanuvchi: [{update.from_user.first_name}]({update.from_user.url}) \n⏳ Ro'yxatdan o'tdi {user.registred}",
                        parse_mode=types.ParseMode.MARKDOWN,
                        reply_markup=DefoltButton.user_home_menu)


@dp.message_handler(commands = 'start')
async def start_registr_handler(update : types.Message, state : FSMContext):
    await db.register_user(update.from_user.id, name=update.from_user.first_name)

    await update.answer(f"Assalomu alaykum [{update.from_user.first_name}]({update.from_user.url}) \n🤖 Men [{db.bot.first_name}]({db.bot.url}) bot man. \n\n👇 O'zingizga kerakli menuyuni tanlang",
                        parse_mode=types.ParseMode.MARKDOWN,
                        reply_markup=DefoltButton.user_home_menu)