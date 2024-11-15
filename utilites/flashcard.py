from data import Word, Unit, DataBase
import random


class Card:
    def __init__(self, 
                 num : int = None,
                 num_at_unit : int = None,  
                 unit : int = None,
                 value : str = None, 
                 answer : str = None) -> None:
        self.value = value
        self.answer = answer
        self.resolt : bool = None
        self.num = num
        self.unit = unit
        self.num_at_unit = num_at_unit

    


def get_question_text(word : Word, order : str) -> str:
    if order == 'defeng' or order == 'defuz':
        text = word.meanig.lower()
        return text.replace(word.value.lower(), "_____")
    elif order == 'uzen':
        return word.translation
    return word.value

def get_question_answer(word : Word, order : str) -> str:
    if order == 'defuz' or order == 'enuz':
        return word.translation
    return word.value

    

def get_cards(units : list[Unit], 
                  order : str = None,
                  mix : bool = False) -> list[Card]:
    cards : list[Card] = []
    for unit in units:
        for word_num, word in unit.words.items():
            question = get_question_text(word, order)
            answer = get_question_answer(word, order)
            cards.append(Card(num_at_unit = word_num, 
                              unit = unit.num,
                              value = question,
                              answer = answer))
    
    if mix:
        random.shuffle(cards)

    for index in range(len(cards)):
        cards[index].num = index + 1
    
    return cards

   


class Flashcards:
    def __init__(self, 
                 book : int = 1, 
                 units : list[Unit] = [],
                 mix : bool = False,
                 order : str = 'enuz') -> None:
        self.total_time : int = 0
        self.book = book
        self.cards = get_cards(units, mix=mix, order=order)
        self.length = len(self.cards)
        self.correct_answers = 0
        self.wrong_answers = 0
        self.answers = []    
        
    
    def get_card(self) -> Card:
        if self.cards:
            return self.cards.pop(0)
    
    def add_answer(self, card : Card):
        if card.resolt:
            self.correct_answers += 1
        else:
            self.wrong_answers += 1

        self.answers.append(card)


    def get_resolts(self):
        return f"""📖 Book {self.book} flashcard natijalari \n\n🔢 Jami savollar: {self.length} \n✅ To'g'ri: {self.correct_answers} \n❌ Xato: {self.wrong_answers}  \n⏳ Vaxt: {self.readable_time}"""

    @property
    def readable_time(self) -> str:
        seconds = self.total_time
        days, seconds = divmod(seconds, 86400) # 86400 seconds in a day
        hours, seconds = divmod(seconds, 3600)  # 3600 seconds in an hour
        minutes, seconds = divmod(seconds, 60)  # 60 seconds in a minute

        # Create a human-readable string
        parts = []
        if days > 0:
            parts.append(f"{days} kun")
        if hours > 0:
            parts.append(f"{hours} soat")
        if minutes > 0:
            parts.append(f"{minutes} minut")
        if seconds > 0 or not parts:
            parts.append(f"{seconds} sec")

        return ', '.join(parts)