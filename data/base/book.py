from .params import UGUtils




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
