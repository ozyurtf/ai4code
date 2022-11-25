# Importing libraries.
import pandas as pd
import os
from subprocess import call
call(["python", "utils.py"])

# Defining the main path.
main_path = '/Users/ozyurtf/Documents/data/ai4code/'

# Importing ancestors data.
train_ancestors = pd.read_csv(main_path + 'train_ancestors.csv')
train_orders = pd.read_csv(main_path + 'train_orders.csv')

# Extracting shuffled cell ids, cell types, and codes/markdowns, and detecting markdown languages for training data.
train_cells_shuffled, train_cell_types_shuffled,train_codes_markdowns_shuffled = [], [], []
for id in train_orders['id']:
    cells_shuffled, cell_types_shuffled,codes_markdowns_shuffled = extract_shuffled_codes_markdowns('train', id)

    train_cells_shuffled.append(cells_shuffled)
    train_cell_types_shuffled.append(cell_types_shuffled)
    train_codes_markdowns_shuffled.append(codes_markdowns_shuffled)

# Including shuffled cells, cell types, codes, markdowns and markdown languages in training data.
train_shuffled_codes_markdowns = pd.DataFrame({'cell_types_shuffled': train_cell_types_shuffled,
                                               'code_markdowns_shuffled': train_codes_markdowns_shuffled,
                                               'cell_shuffled': train_cells_shuffled})
train_final = pd.concat([train_orders, train_shuffled_codes_markdowns], axis=1)
train_final = train_final[['id', 'cell_types_shuffled', 'code_markdowns_shuffled', 'cell_shuffled', 'cell_order']]

# Including the parent and ancestor ids in training data.
train_final = train_final.merge(train_ancestors, on='id', how='left')

# Saving the final training data as csv.
train_final.to_csv('train_final.csv', index=False)

# Extracting the codes and markdowns of test data.
test_jsons = os.listdir(main_path + 'test')

# Extracting shuffled cell ids, cell types, and codes/markdowns, and detecting markdown languages for test data.
test_ids, test_cells_shuffled, test_cell_types_shuffled,test_codes_markdowns_shuffled = [], [], []
for j in test_jsons:
    id = j.replace('.json', '')
    cells_shuffled, cell_types_shuffled,codes_markdowns_shuffled = extract_shuffled_codes_markdowns('test', id)

    test_ids.append(id)
    test_cells_shuffled.append(cells_shuffled)
    test_cell_types_shuffled.append(cell_types_shuffled)
    test_codes_markdowns_shuffled.append(codes_markdowns_shuffled)

# Creating a dataframe of shuffled cells, cell types, codes, markdowns and markdown languages for test data.
test_final = pd.DataFrame({'id': test_ids,
                           'cell_types_shuffled': test_cell_types_shuffled,
                           'code_markdowns_shuffled': test_codes_markdowns_shuffled,
                           'cell_shuffled': test_cells_shuffled})

# Saving the final test data as csv.
test_final.to_csv('test_final.csv', index=False)

