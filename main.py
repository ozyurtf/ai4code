# Importing libraries.
import json
import pandas as pd
import os
from langdetect import detect
import re
from html.parser import HTMLParser
from io import StringIO
import translators as ts

# Defining the main path.
main_path = '/Users/ozyurtf/Documents/data/ai4code/'


def detect_language(text_list):
    try:
        joined_texts = ' '.join(text_list)
        detected_language = detect(joined_texts)
    except:
        detected_language = 'N/A'
    return detected_language


class HTMLStripper(HTMLParser): 
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def clean_markdown(text, puncts_to_remove = '!"#$%&\*+-/;<>\\^_`|~'):
    html_s = HTMLStripper()
    html_s.feed(text)

    text_tags_stripped = html_s.get_data()
    text_encoded = text_tags_stripped

    translator = str.maketrans(puncts_to_remove, ' ' * len(puncts_to_remove))

    text_cleaned = text_encoded.translate(translator)
    text_cleaned = re.sub(' +', ' ', text_cleaned)

    return text_cleaned


def extract_shuffled_codes_markdowns(train_or_test, file_id):
    # Importing codes/markdowns data.
    with open(main_path + '{}/{}.json'.format(train_or_test, file_id)) as f:
        data = json.load(f)

    # Extracting shuffled cell ids, cell types, and codes/markdowns, and detecting markdown languages.
    cells_shuffled = list(data['cell_type'].keys())
    cells_shuffled_joined = ' '.join(cells_shuffled)
    cell_types_shuffled = list(data['cell_type'].values())
    codes_markdowns_shuffled = []
    markdowns_shuffled = []
    for k in data['cell_type'].keys():
        cell_type = data['cell_type'][k]
        if cell_type == 'markdown':
            cleaned_markdowns = clean_markdown(data['source'][k])
            codes_markdowns_shuffled.append(cleaned_markdowns)
            markdowns_shuffled.append(cleaned_markdowns)
        else:
            codes = data['source'][k]
            codes_markdowns_shuffled.append(codes)
    markdown_language = detect_language(markdowns_shuffled)

    # Returning the shuffled cell ids, cell types, codes/markdowns, and markdown languages.
    return cells_shuffled_joined, cell_types_shuffled, codes_markdowns_shuffled, markdown_language


# Importing ancestors data.
train_ancestors = pd.read_csv(main_path + 'train_ancestors.csv')
train_orders = pd.read_csv(main_path + 'train_orders.csv')

# Extracting shuffled cell ids, cell types, and codes/markdowns, and detecting markdown languages for training data.
(train_cells_shuffled, train_cell_types_shuffled,
 train_codes_markdowns_shuffled, train_markdown_languages) = [], [], [], []
for id in train_orders['id']:
    (cells_shuffled, cell_types_shuffled,
     codes_markdowns_shuffled, markdown_language) = extract_shuffled_codes_markdowns('train', id)

    train_cells_shuffled.append(cells_shuffled)
    train_cell_types_shuffled.append(cell_types_shuffled)
    train_codes_markdowns_shuffled.append(codes_markdowns_shuffled)
    train_markdown_languages.append(markdown_language)

# Including shuffled cells, cell types, codes, markdowns and markdown languages in training data.
train_shuffled_codes_markdowns = pd.DataFrame({'cell_types_shuffled': train_cell_types_shuffled,
                                               'code_markdowns_shuffled': train_codes_markdowns_shuffled,
                                               'cell_shuffled': train_cells_shuffled,
                                               'markdown_language': markdown_languages })
train_final = pd.concat([train_orders, train_shuffled_codes_markdowns], axis=1)
train_final = train_final[['id', 'cell_types_shuffled', 'code_markdowns_shuffled',
                           'cell_shuffled', 'cell_order', 'markdown_language']]

# Including the parent and ancestor ids in training data.
train_final = train_final.merge(train_ancestors, on='id', how='left')

# Saving the final training data as csv.
train_final.to_csv('train_final.csv', index=False)

# Extracting the codes and markdowns of test data.
test_jsons = os.listdir(main_path + 'test')

# Extracting shuffled cell ids, cell types, and codes/markdowns, and detecting markdown languages for test data.
(test_ids, test_cells_shuffled, test_cell_types_shuffled,
 test_codes_markdowns_shuffled, test_markdown_languages) = [], [], [], [], []
for j in test_jsons:
    id = j.replace('.json', '')
    (cells_shuffled, cell_types_shuffled,
     codes_markdowns_shuffled, markdown_language) = extract_shuffled_codes_markdowns('test', id)

    test_ids.append(id)
    test_cells_shuffled.append(cells_shuffled)
    test_cell_types_shuffled.append(cell_types_shuffled)
    test_codes_markdowns_shuffled.append(codes_markdowns_shuffled)
    test_markdown_languages.append(markdown_language)

# Creating a dataframe of shuffled cells, cell types, codes, markdowns and markdown languages for test data.
test_final = pd.DataFrame({'id': test_ids,
                           'cell_types_shuffled': test_cell_types_shuffled,
                           'code_markdowns_shuffled': test_codes_markdowns_shuffled,
                           'cell_shuffled': test_cells_shuffled,
                           'markdown_language': test_markdown_languages})

# Saving the final test data as csv.
test_final.to_csv('test_final.csv', index=False)

