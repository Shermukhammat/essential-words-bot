from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


books_icon = {1:"📗", 2:"📕", 3:"📘", 4:"📙", 5:"📔", 6:"📓"}

class InlineButtons:
    books_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = "📗 Book 1", callback_data='1'),InlineKeyboardButton(text = "📕 Book 2", callback_data='2'), InlineKeyboardButton(text = "📘 Book 3", callback_data='3')],
        [InlineKeyboardButton(text = "📙 Book 4", callback_data='4'),InlineKeyboardButton(text = "📔 Book 5", callback_data='5'), InlineKeyboardButton(text = "📓 Book 6", callback_data='6')],
        [InlineKeyboardButton(text= '❌ Bekor qilish', callback_data='cancle')]
    ])

    flashcard_buttons = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("👀 Javobni ko'rish", callback_data="see")]])
    flashcard_buttons_get_answer = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("✅ Topdim", callback_data="correct"), InlineKeyboardButton("❌ Topa olmadim", callback_data='wrong')]])

    def start_flashcard_buttons(random : bool = False, order : str = 'uzeng'):
        if 'defeng' == order:
            uzen = InlineKeyboardButton(text="🛡🔁🇬🇧", callback_data='defeng')
        elif 'defuz' == order:
            uzen = InlineKeyboardButton(text="🛡🔁🇺🇿", callback_data='defuz')
        elif 'uzen' == order:
            uzen = InlineKeyboardButton(text="🇺🇿🔁🇬🇧", callback_data='uzen')
        else:
            uzen = InlineKeyboardButton(text="🇬🇧🔁🇺🇿", callback_data='enuz')

        if random:
            random = InlineKeyboardButton(text="✅ Aralashtirish", callback_data='random_off')
        else:
            random = InlineKeyboardButton(text="🎲 Aralashtirish", callback_data='random_on')

        return InlineKeyboardMarkup(inline_keyboard=[
                    [uzen, random],
                    [InlineKeyboardButton(text="⬅️ Orqaga", callback_data='back'), InlineKeyboardButton(text= '🚀 Flashcardni boshlash', callback_data='start')],
                    [InlineKeyboardButton(text= '❌ Bekor qilish', callback_data='cancle')]])

    def start_test_buttons(uzen : bool = True, random : bool = False, time : int = 10, order : str = 'uzeng'):
        if 'defeng' == order:
            uzen = InlineKeyboardButton(text="🛡🔁🇬🇧", callback_data='defeng')
        elif 'defuz' == order:
            uzen = InlineKeyboardButton(text="🛡🔁🇺🇿", callback_data='defuz')
        elif 'uzen' == order:
            uzen = InlineKeyboardButton(text="🇺🇿🔁🇬🇧", callback_data='uzen')
        else:
            uzen = InlineKeyboardButton(text="🇬🇧🔁🇺🇿", callback_data='enuz')

        if random:
            random = InlineKeyboardButton(text="✅ Aralashtirish", callback_data='random_off')
        else:
            random = InlineKeyboardButton(text="🎲 Aralashtirish", callback_data='random_on')

        return InlineKeyboardMarkup(inline_keyboard=[
                    get_time_buttons(time),
                    [uzen, random],
                    [InlineKeyboardButton(text="⬅️ Orqaga", callback_data='back'), InlineKeyboardButton(text= '🚀 Testni boshlash', callback_data='start')],
                    [InlineKeyboardButton(text= '❌ Bekor qilish', callback_data='cancle')]])

    def wordlist_buttons(book : int, unit  : int, forbid_photo : bool = False):
        if forbid_photo:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🖼 Rasm", callback_data='x'), InlineKeyboardButton(text="🎧 Audio", switch_inline_query_current_chat=f"{book}&{unit}")]
                ]
            )
        return InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🖼 Rasm", callback_data=f"{book}&{unit}"), InlineKeyboardButton(text="🎧 Audio", switch_inline_query_current_chat=f"{book}&{unit}")]
                ]
            )
    
    def unit_buttons(selected : list[int], book : int = 1):
        icon = books_icon.get(book, "📗")
        buttons = []
        for n in range(1, 30, 3):
            row = []
            for i in range(n, n+3):
                if i in selected:
                    row.append(InlineKeyboardButton(text=f"✅ Unit {i}", callback_data=f'u{i}'))
                else:
                    row.append(InlineKeyboardButton(text=f"{icon} Unit {i}", callback_data=f"s{i}"))
            buttons.append(row)

        if selected:
            buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data='back'), InlineKeyboardButton(text="➡️ Keyingi", callback_data='next')])
        else:
            buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data='back')])
        
        buttons.append([InlineKeyboardButton(text= '❌ Testni bekor qilish', callback_data='cancle')])
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    



def get_time_buttons(time : int):
    time_buttons = []
    for time_, icon in {10:"🐎", 20:"🐇", 30:"🐢"}.items():
        if time_ == time:
            time_buttons.append(InlineKeyboardButton(f"✅ {time_} sec", callback_data=f'time&{time_}'))
        else:
            time_buttons.append(InlineKeyboardButton(f"{icon} {time_} sec", callback_data=f'time&{time_}'))

    return time_buttons