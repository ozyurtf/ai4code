# Importing libraries.
import json
import pandas as pd

# Definin the main path.
main_path = '/Users/ozyurtf/Documents/data/ai4code/'

# Importing data.
train_ancestors = pd.read_csv(main_path + 'train_ancestors.csv')
train_orders = pd.read_csv(main_path + '/train_orders.csv')

# Sample ID in training data.
train_sample_id = '00015c83e2717b'

# Opening a sample training json file.
with open(main_path + 'train/{}.json'.format(train_sample_id)) as f:
    train_data = json.load(f)

# Printing codes and markdowns.
print("Codes:")
print('-------------------------------------------------------------')
print("\n".join([train_data['source'][val] for val in code_ids]))
print()
print('-------------------------------------------------------------')
print("Markdowns:")
print('-------------------------------------------------------------')
print("\n".join([train_data['source'][val] for val in markdown_ids]))
print()
print('-------------------------------------------------------------')
print("Cell Order:")
print('-------------------------------------------------------------')
cell_order = train_orders[train_orders['id'].apply(lambda x: x == '00015c83e2717b')]['cell_order'].values[0].split(' ')
print('\n'.join([train_data['source'][val] for val in cell_order]))
print('-------------------------------------------------------------')

# Sample ID in test data.
test_sample_id = '0010a919d60e4f'

# Opening a sample training json file.
with open(main_path + 'test/{}.json'.format(test_sample_id)) as f:
    test_data = json.load(f)


# Separating codes and markdowns.
code_ids = []
markdown_ids = []
for k in test_data['cell_type'].keys():
    cell_type = test_data['cell_type'][k]
    if cell_type=='code':
        code_ids.append(k)
    else:
        markdown_ids.append(k)


# Printing codes and markdowns.
print("Codes:")
print('-------------------------------------------------------------')
print("\n".join([test_data['source'][val] for val in code_ids]))
print()
print('-------------------------------------------------------------')
print("Shuffled Markdowns:")
print('-------------------------------------------------------------')
print("\n".join([test_data['source'][val] for val in markdown_ids]))
print()
print('-------------------------------------------------------------')

