with open("SECRETKEY.txt", "r") as f:
    key = f.read()
    key = key.split('\n')[1]

url = "https://us-central1-aiplatform.googleapis.com/v1/projects/skillup-405602/locations/us-central1/publishers/google/models/textembedding-gecko:predict"
command = ["curl", "-X","POST", "-H", f"Authorization: Bearer {key}", "-H", "Content-Type: application/json; charset=utf-8", "-d", "@embeddings/request.json", url]

import pandas as pd
import json
from subprocess import run, CalledProcessError
 
"""def get_embedding(string):
    with open("embeddings/request.json", "w") as f:
        json_obj = {
                    "instances": [
                    { 
                        "content": string
                    }
                    ]
                }
        f.write(json.dumps(json_obj))
    
    for i in range(10): 
        try:
            process = run(command, capture_output=True, timeout= 10)
            if (process.returncode == 0):
                return json.loads(process.stdout)['predictions'][0]['embeddings']['values']
        except CalledProcessError as e:
            print(f"Error is {e}")
            pass
        except Exception as e:
            print(f" Unexpected Error is {e}")
            pass
    return []"""

from transformers import AutoModel, AutoTokenizer

def get_embedding(string):
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    model = AutoModel.from_pretrained("roberta-base")

    tokens = tokenizer("hello world", return_tensors="pt", truncation=True)
    response = model(**tokens)
    return response.pooler_output[0].tolist()




    
# print(get_embedding("sasldkjasdffh"*1600))

def get_embeddings(strings):
    embeddings = []
    for string in strings:
        embeddings.append(get_embedding(string))
    return embeddings

def get_embeddings_csv(filename):
    df = pd.read_csv(filename)
    texts = list(df['text'])
    return get_embeddings(texts)


"""embeddings_one = get_embeddings(["hello", "my name is Varun"])
# print(get_embeddings(["hello", "my name is Varun"]))
print (f"This is get_embeddings pos 0 {embeddings_one[0]}")
print (f"This is get_embeddings pos 1 {embeddings_one[1]}")
"""