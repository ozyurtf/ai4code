import ast
import pandas as pd

pd.read_csv('tra')


train_final['codes'] = train_final['codes'].apply(ast.literal_eval)
train_final['markdowns'] = train_final['markdowns'].apply(ast.literal_eval)


test_final['codes'] = test_final['codes'].apply(ast.literal_eval)
test_final['markdowns'] = test_final['markdowns'].apply(ast.literal_eval)