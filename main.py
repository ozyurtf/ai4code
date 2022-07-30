import json

f = open('/Users/ozyurtf/Documents/data/AI4Code/train/0a0b0188aa37ca.json')

data = json.load(f)

f.close()

code_ids = []
markdown_ids = []
for k in data['cell_type'].keys():
    cell_type = data['cell_type'][k]
    if cell_type=='code':
        code_ids.append(k)
    else:
        markdown_ids.append(k)

print("Codes:")
print("\n".join([data['source'][val] for val in code_ids]))
print()
print("###########")
print()
print("Markdowns:")
print("\n".join([data['source'][val] for val in markdown_ids]))



