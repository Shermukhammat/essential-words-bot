from .params import UGUtils
from .cache import Cache
import json, sqlite3


class BookData:
    def __init__(self, path : str) -> None:
        self.path = path
        self.utilts = UGUtils(path)
        self.data = self.utilts.get_yaml()

        self.book_num : int = self.data.get('book', 1)
        units : dict = self.data.get('units', {})
        self.units : dict[int, Unit] = {key : Unit(key, value, book_num=self.book_num) for key, value in units.items()}
        
                

books = {1: "📗", 2: "📕", 3: "📘", 4: "📙", 5: "📔", 6: "📓"}

class Unit:
    def __init__(self, unit : int, unit_data : dict, book_num : int = 1) -> None:
        self.book_num = book_num
        self.num = unit
        self.words : dict[int, Word] = {positon : Word(word_data) for positon, word_data in unit_data.get('words', {}).items()}
        self.photos_id : list[int] = [photo_id for photo_id in unit_data.get('photos', [])]
        self.data = unit_data
        self.text = self.get_words_text()

    def get_words_text(self) -> str:
        book_icon = books.get(self.book_num, "📗")
        # Use Markdown for formatting; if using HTML, replace `**` with <b>...</b>
        text = f"{book_icon} **Book {self.book_num}**  Unit {self.num}\n\n"
    
        # Add icons for meaning and translation
        for position, word in self.words.items():
            text += f"{position}  {word.value} - _{word.translation}_\n"
        
        return text

    

class Word:
    def __init__(self, data : dict) -> None:
        self.value : str = data.get('word', 'none')
        self.translation : str = data.get('translation', 'none')
        self.audio_id : int = data.get('audio')
        self.meanig : str = data.get('meaning')
        self.meanig_tr : str = data.get('meaning_tr')
        self.example : str = data.get('example')
        self.example_tr : str = data.get('example_tr')
        self.type : str = data.get('type')





class BookData2:
    def __init__(self, path : str) -> None:
        self.path = path
        self.books : dict[int, Cache]  = {n : Cache() for n in range(1, 7)}


    async def get_unit(self, book : int, unit : int) -> Unit:
        answer = await self.books[book].get(unit)
        if answer:
            return answer
        
        answer = get_unit_from_db(self.path, unit, book)
        if answer:
            await self.books[book].set(unit, answer)
            return answer
        
    async def set_unit(self, unit : Unit):
        if add_words(self.path, unit):
            if self.books.get(unit.book_num):
                await self.books[unit.book_num].set(unit.num, unit)
        


def add_words(path : str, unit : Unit) -> bool:
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    id = f"{unit.book_num}{unit.num}"
    if id.isnumeric():
        id = int(id)
    else:
        raise Exception("add_words: unit num or book nom no found")
    
    cur.execute(""" INSERT INTO units(id, data) VALUES(?, ?);""", (id, json.dumps(unit.data)))  

    conn.commit()
    conn.close()

    return True
    

def get_unit_from_db(path : str, unit : int, book : int) -> Unit:
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    for row in cur.execute(f""" SELECT data FROM units WHERE id = {book}{unit};"""):
        conn.close()
        data = json.loads(row[0])
        return Unit(unit, data, book_num=book)

    conn.close()