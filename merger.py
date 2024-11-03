import pandas as pd
import yaml, os
from ruamel.yaml import YAML


class ConfigurationYaml:
    def __init__(
        self,
        mapping: int = 2,
        sequence: int = 4,
        offset: int = 2,
        default_fs: bool = False,
        enc: str = "utf-8",
    ) -> None:
        yaml2 = YAML()
        yaml2.indent(mapping=mapping, sequence=sequence, offset=offset)
        yaml2.default_flow_style = default_fs
        yaml2.encoding = enc
        self.yaml_conf = yaml2


class UGUtils:
    def __init__(self, yaml_file: str) -> None:
        self.path = yaml_file
        self.data = self.get_yaml()
    def get_yaml(self) -> dict:
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as file:
                file.write("")

        with open(self.path, encoding="utf-8") as file:
            data = yaml.safe_load(file)

            if not data:
                return {}
            return data


    def update_yaml(self, data: dict):
        yaml_config = ConfigurationYaml().yaml_conf
        with open(self.path, "w", encoding="utf-8") as file:
            data = yaml_config.dump(data, file)

        if data:
            return data
        return {}
    


# yamlut = UGUtils('data/test.yaml')

# yamlut.update_yaml({'salom' : "blah"})

def get_unit(book : int = 1, 
             unit : int = 1, 
             data : pd.DataFrame = None) -> pd.DataFrame:
    return data[(data['book'] == book) & (data['unit'] == unit)]


screenshots = pd.read_csv('screenshots2.csv')
words_data = pd.read_csv('row_data4.csv')

for book_num in range(1, 7):
    yamlut = UGUtils(f'data/book{book_num}.yaml')
    bookdata = {'book': book_num,
                'units': {},
                'appendix' : []}
    
    for unit_num in range(1, 31):
        unit = get_unit(book=book_num, unit=unit_num, data=words_data)
        unitwords = {}
        for word_num, word_index in enumerate(unit.index):
            unitwords[word_num + 1] = {
            'word' : unit.loc[word_index, 'word'],
            'translation' : unit.loc[word_index, 'translation'],
            'audio' : int(unit.loc[word_index, 'sound1_data_id']),
            'meaning' : unit.loc[word_index, 'mean'],
            'example' : unit.loc[word_index, 'example'],
            'type' : unit.loc[word_index, 'type'],
            'meaning_tr' : unit.loc[word_index, 'mean_tr'],
            'example_tr' : unit.loc[word_index, 'example_tr']
            }

        #wordlist_photo1_data_id,wordlist_photo2_data_id,exercise_photo1_data_id,exercise_photo2_data_id,story_photo_data_id,story_exercise_photo_data_id
        screenshot = screenshots[(screenshots['book'] == book_num) & (screenshots['unit'] == unit_num)]
        screenshot = screenshot.to_dict()
        # print(screenshot)
        wordlis1 = [n for n in screenshot['wordlist_photo1_data_id'].values()][0]
        wordlis2 = [n for n in screenshot['wordlist_photo2_data_id'].values()][0]
        exercise1 = [n for n in screenshot['exercise_photo1_data_id'].values()][0]
        exercise2 = [n for n in screenshot['exercise_photo2_data_id'].values()][0]
        story = [n for n in screenshot['story_photo_data_id'].values()][0]
        story_exercise = [n for n in screenshot['story_exercise_photo_data_id'].values()][0]

        unit_data = {
            'words' : unitwords,
            'photos' : [wordlis1, wordlis2],
            'exercise' : [exercise1, exercise2],
            'reading' : {'photo':[story, story_exercise], 
                         'audio' : None}
        }
        bookdata['units'][unit_num] = unit_data
        # print(unit_data)

    # print(bookdata)
    yamlut.update_yaml(bookdata)





    print(book_num)


