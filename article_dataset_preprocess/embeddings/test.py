from transformers import AutoModel, AutoTokenizer
from datasets import Dataset

tokenizer = AutoTokenizer.from_pretrained("roberta-base")
model = AutoModel.from_pretrained("roberta-base")

tokens = tokenizer("hello world", return_tensors="pt", truncation=True)
response = model(**tokens)
print(response.pooler_output[0].tolist())