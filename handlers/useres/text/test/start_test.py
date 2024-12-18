from loader import dp, db, bot
from utilites.states.useres import UserState
from utilites.buttons import DefoltButton, InlineButtons
from utilites import shoud_edit
from aiogram.dispatcher import FSMContext
from aiogram import types

@dp.message_handler(state=UserState.test.start_test)
async def start_tes_text(update : types.Message, state : FSMContext):
    state_data = await state.get_data()
    selected = str(state_data.get('selected'))
    order = state_data.get('order')
    book = state_data.get('book')
    time = state_data.get('time')
    random = state_data.get('random')
    random_text, uzen_text = get_texts(order, random)
        
    
    await update.answer(f"❌ Testni bekor qilish uchun `bekor qilish` tugmasni bosing  \n\n📖 Book {book} Test\n \n🔢 Unitlar: `{selected[1:-1]}` \n⏳ Vaxt harbir test uchun: `{time} sec` \n🎲 Aralashtirish: `{random_text}` \n{uzen_text}",
                        parse_mode=types.ParseMode.MARKDOWN,
                        reply_markup=InlineButtons.start_test_buttons(order = order, random = random, time = time))


def get_texts(order : str, random : bool):
    if random:
        random_text = 'yoniq'
    else:
        random_text = 'o\'chiq'
    
    if order == 'defeng':
        uzen_text = "❓ Savol: `🛡 Definiton` \n🧩Variyantlar: `🇬🇧 Inglizcha`"
    elif order == 'defuz':
        uzen_text = "❓ Savol: `🛡 Definiton` \n🧩Variyantlar: `🇺🇿 O'zbekcha`"
    elif order == 'uzen':
        uzen_text = "❓ Savol: `🇺🇿 O'zbekcha` \n🧩Variyantlar: `🇬🇧 Inglizcha`"
    else:
        uzen_text = "❓ Savol: `🇬🇧 Inglizcha` \n🧩Variyantlar: `🇺🇿 O'zbekcha`"
    
    return random_text, uzen_text