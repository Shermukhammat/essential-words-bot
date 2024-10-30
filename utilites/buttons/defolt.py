from aiogram.types import KeyboardButton, ReplyKeyboardMarkup



def get_book_buttons(book : str = "📗", unit : int = 1) -> ReplyKeyboardMarkup:
    unists  = get_unit_buttons(book=book)
    
    unists.insert(0, [KeyboardButton(f"⬇️{book} Yuklash"), KeyboardButton(f"{book} APPENDIX")])
    unists.append([KeyboardButton("❓ Test"), KeyboardButton("🀄️ Flashcard")])
    unists.append([KeyboardButton("⬅️ Orqaga")])

    return ReplyKeyboardMarkup(keyboard=unists, resize_keyboard=True) 


def get_unit_buttons(book : str = "📗", 
                    start : int = 1, 
                    stop : int = 31, 
                    step : int = 3) -> list[list[KeyboardButton]]:    
    return [[KeyboardButton(f"{book} Unit {n}"), KeyboardButton(f"{book} Unit {n+1}"), KeyboardButton(f"{book} Unit {n+2}")] for n in range(start, stop, step)]



books = [get_book_buttons(book=book) for book in ["📗", "📕", "📘", "📙", "📔", "📓"]]
books_icon = ["📗", "📕", "📘", "📙", "📔", "📓"]
class DefoltButton:
    user_home_menu = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("📗 Book 1"),KeyboardButton("📕 Book 2"), KeyboardButton("📘 Book 3")],
                [KeyboardButton("📙 Book 4"),KeyboardButton("📔 Book 5"), KeyboardButton("📓 Book 6")],
                [KeyboardButton("❓ Test"), KeyboardButton("🀄️ Flashcard")],
                [KeyboardButton("ℹ️ Yordam")]
            ],
            resize_keyboard=True
        )


    def get_book_menu(book : int) -> ReplyKeyboardMarkup:
        if book <= 6 and book >= 1:
            return books[book - 1]
    
    def get_unit_menu(unit : int = 1, book : int = 1) -> ReplyKeyboardMarkup:
        if unit >= 1 and unit <= 30 and book >= 1 and book <= 6:
            icon = books_icon[book - 1]

            return ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(f"{icon} Word list {unit}"), KeyboardButton(f"{icon} Reading {unit}")],
                [KeyboardButton(f"{icon} Exercise {unit}")],
                [KeyboardButton("⬅️ Orqaga"), KeyboardButton("🎛 Bosh menu")]
            ], resize_keyboard = True)

    book1_menu : ReplyKeyboardMarkup = get_book_buttons(book="📗")