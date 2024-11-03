from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




class InlineButtons:
    def wordlist_buttons(book : int, unit  : int, forbid_photo : bool = False):
        if forbid_photo:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🖼 Rasim", callback_data='x'), InlineKeyboardButton(text="🎧 Audio", switch_inline_query_current_chat=f"{book}&{unit}")]
                ]
            )
        return InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🖼 Rasim", callback_data=f"{book}&{unit}"), InlineKeyboardButton(text="🎧 Audio", switch_inline_query_current_chat=f"{book}&{unit}")]
                ]
            )