# Importing libraries.
import json
import pandas as pd

# Importing data.
train_ancestors = pd.read_csv('/Users/ozyurtf/Documents/data/AI4Code/train_ancestors.csv')
train_orders = pd.read_csv('/Users/ozyurtf/Documents/data/AI4Code/train_orders.csv')
sample_submission = pd.read_csv('/Users/ozyurtf/Documents/data/AI4Code/sample_submission.csv')

# Opening a sample training json file.
with open('/Users/ozyurtf/Documents/data/AI4Code/test/0010a919d60e4f.json') as f:
    train_data = json.load(f)

# Opening a sample test json file.
with open('/Users/ozyurtf/Documents/data/AI4Code/test/0010a919d60e4f.json') as f:
    test_data = json.load(f)

# Separating codes and markdowns.
code_ids = []
markdown_ids = []
for k in train_data['cell_type'].keys():
    cell_type = train_data['cell_type'][k]
    if cell_type=='code':
        code_ids.append(k)
    else:
        markdown_ids.append(k)

# Printing codes and markdowns.
print("Codes:")
print("\n".join([train_data['source'][val] for val in code_ids]))
print()
print("###########")
print()
print("Markdowns:")
print("\n".join([train_data['source'][val] for val in markdown_ids]))
print()
