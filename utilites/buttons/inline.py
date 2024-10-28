from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




class InlineButtons:
    def wordlist_buttons(book : int, unit  : int):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🖼 Rasim", callback_data=f"photo={book}&unit={unit}"), InlineKeyboardButton(text="🎧 Audio", switch_inline_query_current_chat=f"book{book}.unit{unit}")]
            ]
        )