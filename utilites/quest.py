from data import Word, Unit, DataBase
import random


class Question:
    def __init__(self, 
                 num : int = None,
                 num_at_unit : int = None,  
                 unit : int = None,
                 value : str = None, 
                 answer : str = None,
                 options : list[str] = []) -> None:
        self.value = value
        self.answer_index = 0
        self.answer = answer
        self.options = options
        self.resolt : bool = None
        self.num = num
        self.unit = unit
        self.num_at_unit = num_at_unit

    def check_answer(self, index : int):
        if len(self.options) > index:
            self.resolt = self.options[index] == self.answer
        
    
    def add_options(self, options : list[str]):
        self.options = options
        self.options.append(self.answer)
        random.shuffle(self.options)
        self.answer_index = self.options.index(self.answer)
    


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


def get_options(options : list[str], ignore : str) -> list[str]:
    options = [option for option in options if option != ignore]
    if len(options) < 3:
        return options
    else:
        return random.sample(options, 3)
    

def get_questions(units : list[Unit], 
                  order : str = None,
                  mix : bool = False) -> list[Question]:
    questions : list[Question] = []
    options = []
    for unit in units:
        for word_num, word in unit.words.items():
            question = get_question_text(word, order)
            answer = get_question_answer(word, order)
            options.append(answer)
            questions.append(Question(num_at_unit = word_num, 
                                   unit = unit.num,
                                   value = question,
                                   answer = answer))
    
    for index, question in enumerate(questions):
        questions[index].add_options(get_options(options, question.answer))
    
    if mix:
        random.shuffle(questions)

    for index, question in enumerate(questions):
        questions[index].num = index + 1
    
    return questions

   


class Test:
    def __init__(self, 
                 book : int = 1, 
                 units : list[Unit] = [],
                 time : int = 10,
                 mix : bool = False,
                 order : str = 'enuz') -> None:
        self.total_time : int = 0
        self.time = time
        self.book = book
        self.questions = get_questions(units, mix=mix, order=order)
        self.length = len(self.questions)
        self.correct_answers = 0
        self.wrong_answers = 0
        self.skiped = 0
        self.answers = []    
        
    
    def get_question(self) -> Question:
        if self.questions:
            return self.questions.pop(0)
    
    def add_answer(self, question : Question):
        if question.resolt == True:
            self.correct_answers += 1
        elif question.resolt == False:
            self.wrong_answers += 1
        else:
            self.skiped += 1

        self.answers.append(question)

    def get_resolts(self):\
        return f"""📖 Book {self.book} test natijalari \n\n🔢 Jami savollar: {self.length} \n✅ To'g'ri: {self.correct_answers} \n❌ Xato: {self.wrong_answers} \n➡️Javob berilmadi: {self.skiped}  \n⏳ Vaxt: {self.readable_time}"""

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