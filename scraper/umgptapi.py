from openai import AzureOpenAI

with open("SECRETKEY.txt", "r") as f:
    key = f.read()
    key = key.split('\n')[0]

client = AzureOpenAI(api_key=key,
azure_endpoint='https://api.umgpt.umich.edu/azure-openai-api/ptu',
api_version='2023-03-15-preview')

import re
import numpy as np

import pandas as pd

filenum = input("which file num? ")
indf = pd.read_csv(f"scraper/extracted_text{filenum}.csv")
indf = indf.replace("", np.NaN)
indf = indf.dropna()

print(indf)
outdict = {"index": [], "text": [], "url": []}

for index, row in indf.iterrows():
    text = re.sub(r'[^a-zA-Z0-9\._-]', '', row['text'])

    print(f"this raw article contains {len(text)} characters")
    final_response = np.NaN
    if (len(text) < 1000):
        print(text) #print to understand why there is an error
    else:

        text = text[:min(len(text), 31000)]
        """for i in range(0, len(text), 20000): #4 characters per token and we want to feed roughly 8000 tokens so we can get a good response back
            split_text.append(text[i:min(len(text), i+20000)])"""

        response = client.chat.completions.create(model='gpt-4',
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Remove words that don't relate to the main themes of to the article deliminated by triple quotes\n" + f'"""{text}"""'}
        ])
        final_response = response.choices[0].message.content

    outdict["index"].append(index)
    outdict["text"].append(final_response)
    outdict["url"].append(row['url'])

    print(f"article {index} done")
# print the response
outdf = pd.DataFrame(data = outdict)
outdf.to_csv(f"scraper/cleaned_extracted_text{filenum}.csv")
