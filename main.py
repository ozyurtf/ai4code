# Importing libraries.
import json
import pandas as pd

# Defining the main path.
main_path = '/Users/ozyurtf/Documents/data/ai4code/'

# Importing data.
train_ancestors = pd.read_csv(main_path + 'train_ancestors.csv')
train_orders = pd.read_csv(main_path + 'train_orders.csv')


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
