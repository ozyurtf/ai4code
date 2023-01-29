import pandas as pd
import ast
from torch.nn import Linear, Tanh
from torch import no_grad, mm
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")

train_final = pd.read_csv('data/train_final.csv', nrows = 1000, converter = {'cell_type_shuffled': ast.literal_eval,
                                                                             'code_markdown_shuffled': ast.literal_eval,
                                                                             'cell_order_shuffled': ast.literal_eval,
                                                                             'cell_rank_shuffled': ast.literal_eval,
                                                                             'cell_order': ast.literal_eval})

train_final_exploded = train_final.explode(['cell_type_shuffled',
                                            'code_markdown_shuffled',
                                            'cell_order_shuffled', 
                                            'cell_rank_shuffled',
                                            'cell_order']).reset_index(drop=True)

notebook_example = train_final_exploded.query('id == "00001756c60be8"')

codes = notebook_example.query('cell_type_shuffled == "code"')['code_markdown_shuffled']
markdowns = notebook_example.query('cell_type_shuffled == "markdown"')['code_markdown_shuffled']

codes_tokenized = tokenizer(codes.tolist(), padding=True, truncation=True, return_tensors="pt")
markdowns_tokenized = tokenizer(markdowns.tolist(), padding=True, truncation=True, return_tensors="pt")

codes_input_ids, codes_attention_masks = codes_tokenized.values()
markdowns_input_ids, markdowns_attention_masks = markdowns_tokenized.values()

with no_grad():
    codes_embeddings = model(codes_input_ids, attention_mask=codes_attention_masks)
    markdowns_embeddings = model(markdowns_input_ids, attention_mask=markdowns_attention_masks)
    
markdowns_attention_masks_unsq = markdowns_attention_masks.unsqueeze(-1)

markdown_embeddings_scaled = (markdowns_embeddings[0] * markdowns_attention_masks_unsq).sum(1) / markdowns_attention_masks_unsq.sum(1)

linear = Linear(768, 768)(markdown_embeddings_scaled)
tanh = Tanh()(linear)

print(tanh)
