from googletrans import Translator
import pandas as pd
from time import sleep


tr = Translator()

def translet(text : str) -> str:
    answer = tr.translate(text, src='en', dest='uz')
    if answer:
        return answer.text
    


data = pd.read_csv('row_data3.csv')

# data['mean_tr'] = None
# data['example_tr'] = None

for index, mean in enumerate(data['mean']):
    if data.loc[index, 'mean_tr']:
        continue

    sleep(0.2)

    mean_tr = translet(mean)
    data.at[index, 'mean_tr'] = mean_tr

    print(f"meaning updated at index:{index}            ", end='\r')
    data.to_csv('row_data3.csv', index_label=False)


for index, example in enumerate(data['example']):
    if type(data.loc[index, 'example_tr']) != float or type(data.loc[index, 'example_tr']) == str:
        continue

    sleep(0.2)
    example_tr = translet(example)
    data.at[index, 'example_tr'] = example_tr

    print(f"example updated at index:{index}            ", end='\r')
    data.to_csv('row_data3.csv', index_label=False)

print("Finished")
