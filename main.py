# Importing libraries.
import json
import pandas as pd
import os
from langdetect import detect
import ast

# Defining the main path.
main_path = '/Users/ozyurtf/Documents/data/ai4code/'

# Importing data.
train_ancestors = pd.read_csv(main_path + 'train_ancestors.csv')
train_orders = pd.read_csv(main_path + 'train_orders.csv')
sample_submission = pd.read_csv(main_path + 'sample_submission.csv')


def extract_codes_markdowns(train_or_test, code_or_markdown, file_id):
    # Importing data.
    with open(main_path + '{}/{}.json'.format(train_or_test, file_id)) as f:
        data = json.load(f)

    # Extracting codes/markdowns.
    code_or_markdown_list = []
    for k in data['cell_type'].keys():
        cell_type = data['cell_type'][k]
        if cell_type == code_or_markdown:
            code_or_markdown_list.append(data['source'][k])
        else:
            pass
    # Returning the list of codes/markdowns.
    return code_or_markdown_list


def detect_language(text_list):
    try:
        joined_texts = ' '.join(text_list)
        detected_language = detect(joined_texts)
    except:
        detected_language = 'N/A'
    return detected_language


# Extracting the codes in training data.
train_codes = train_orders['id'].apply(lambda x: extract_codes_markdowns(train_or_test='train',
                                                                         code_or_markdown='code',
                                                                         file_id=x))

# Extracting the markdowns in training data
train_markdowns = train_orders['id'].apply(lambda x: extract_codes_markdowns(train_or_test='train',
                                                                             code_or_markdown='markdown',
                                                                             file_id=x))

# Including codes and markdowns in training data.
train_codes_markdowns = pd.concat([train_codes, train_markdowns], axis=1)
train_codes_markdowns.columns = ['codes', 'markdowns']
train_final = pd.concat([train_orders, train_codes_markdowns], axis=1)
train_final = train_final[['id', 'codes', 'markdowns', 'cell_order']]

# Detecting the language of the markdowns in training data.
train_final['language'] = train_final['markdowns'].apply(detect_language)

# Extracting the codes and markdowns from each json file in test data.
test_jsons = os.listdir(main_path + 'test')
test_codes = []
test_markdowns = []
test_ids = []
for j in test_jsons:
    test_id = j.replace('.json', '')
    test_code = extract_codes_markdowns(train_or_test='test',
                                        code_or_markdown='code',
                                        file_id=test_id)
    test_markdown = extract_codes_markdowns(train_or_test='test',
                                            code_or_markdown='markdown',
                                            file_id=test_id)

    test_ids.append(test_id)
    test_codes.append(test_code)
    test_markdowns.append(test_markdown)

# Creating a dataframe for test set similar to the one we prepared for training set.
test_final = pd.DataFrame({'id': test_ids,
                           'codes': test_codes,
                           'markdowns': test_markdowns})

# Including the cell order to the test dataframe.
test_final = test_final.merge(sample_submission, on ='id', how='left')

# Detecting the language of the markdowns in test data.
test_final['language'] = test_final['markdowns'].apply(detect_language)

# Saving the final training data as csv.
train_final.to_csv('train_final.csv', index=False)

# Saving the final test data as csv.
test_final.to_csv('test_final.csv', indeex=False)