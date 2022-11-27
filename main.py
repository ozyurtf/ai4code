# Importing libraries.
import pandas as pd
import os
from multiprocess import Pool
from functools import partial
from utils import *

# Importing training and test data.
train_ancestors = pd.read_csv('data/train_ancestors.csv').reset_index(drop=True)
train_orders = pd.read_csv('data/train_orders.csv').reset_index(drop=True)
test_jsons = os.listdir('data/test')
train_ids = train_orders['id']
test_ids = [val.replace('.json', '') for val in test_jsons]

# Extracting shuffled cells, cell types, and codes/markdowns for both training and test data.
pool = Pool(6)
partial_train = partial(extract_shuffled_codes_markdowns, train_test = 'train')
partial_test = partial(extract_shuffled_codes_markdowns, train_test = 'test')

(train_cell_types_shuffled,
 train_cell_orders_shuffled,
 train_codes_markdowns_shuffled) = zip(*pool.map_async(partial_train, train_ids).get())

(test_cell_types_shuffled,
 test_cell_orders_shuffled,
 test_codes_markdowns_shuffled) = zip(*pool.map_async(partial_test, test_ids).get())

pool.close()
pool.join()

# Including shuffled cells, cell types, codes, markdowns and markdown languages in training data.
train_shuffled_codes_markdowns = pd.DataFrame({'cell_type_shuffled': train_cell_types_shuffled,
                                               'cell_order_shuffled': train_cell_orders_shuffled,
                                               'code_markdown_shuffled': train_codes_markdowns_shuffled})
train_final = pd.concat([train_orders, train_shuffled_codes_markdowns], axis=1)
train_final['cell_order'] = train_final['cell_order'].apply(lambda x: x.split(' '))

cell_ranks_shuffled = []
for x in range(train_final.shape[0]):
    cell_order_shuffled = train_final['cell_order_shuffled'][x]
    cell_order = train_final['cell_order'][x]
    cell_rank_map = dict(zip(cell_order, range(len(cell_order))))
    cell_rank_shuffled = [cell_rank_map[val] for val in cell_order_shuffled]
    cell_ranks_shuffled.append(cell_rank_shuffled)

train_final['cell_rank_shuffled'] = cell_ranks_shuffled
train_final = train_final[['id', 'cell_type_shuffled', 'code_markdown_shuffled',
                           'cell_order_shuffled', 'cell_rank_shuffled', 'cell_order']]

# Including the parent and ancestor ids in training data.
train_final = train_final.merge(train_ancestors, on='id', how='left')

# Saving the final training data as csv.
train_final.to_csv('data/train_final.csv', index=False)

# Creating a dataframe of shuffled cells, cell types, codes, markdowns and markdown languages for test data.
test_final = pd.DataFrame({'id': test_ids,
                           'cell_type_shuffled': test_cell_types_shuffled,
                           'code_markdown_shuffled': test_codes_markdowns_shuffled,
                           'cell_order_shuffled': test_cell_orders_shuffled})

# Saving the final test data as csv.
test_final.to_csv('data/test_final.csv', index=False)

