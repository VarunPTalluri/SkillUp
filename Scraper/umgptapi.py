import os
from openai import AzureOpenAI

client = AzureOpenAI(api_key='b4074b8eacf64b4fb201800c9ad60a6f',
azure_endpoint='https://api.umgpt.umich.edu/azure-openai-api/ptu',
api_version='2023-03-15-preview')

import json

import pandas as pd

indf = pd.read_csv("Scraper/extracted_text.csv")
outdict = {"index": [], "text": [], "url": []}

for index, row in indf.iterrows():
    text = row['text']
    response = client.chat.completions.create(model='gpt-4',
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "\nCan you remove words that don't relate to the main themes of the article deliminated by triple quotes\n" + f'"""{text}"""'}
    ])
    outdict["index"].append(index)
    outdict["text"].append(response.choices[0].message.content)
    outdict["url"].append(row['url'])

    print(f"article {index} done")
# print the response
outdf = pd.DataFrame(data = outdict)
outdf.to_csv("Scraper/cleaned_extracted_text.csv")