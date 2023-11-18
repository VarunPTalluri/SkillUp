import os
from openai import AzureOpenAI

client = AzureOpenAI(api_key='b4074b8eacf64b4fb201800c9ad60a6f',
azure_endpoint='https://api.umgpt.umich.edu/azure-openai-api/ptu',
api_version='2023-03-15-preview')

import json

import pandas as pd

"""df = pd.read_csv("Scraper/extracted_text.csv")

print(df)"""

with open("Scraper/onearticle.txt") as f:
    text = f.read()
with open("Scraper/resultwanted.txt") as f:
    output = f.read()
with open("Scraper/inputwanted.txt") as f:
    input_ = f.read()

response = client.chat.completions.create(model='gpt-4',
messages=[
    {"role": "system", "content": "You are a helpful assistant"},
    #{"role": "user", "content": text + "\n can you explain the article in such a way that it can train another GPT agent with no prior knowledge"}
    {"role": "user", "content": "Can you remove the extra words here: " input_ + "\n this in the output\n" + output + "\n" text + "\n can you remove the extra words?"}
])

# print the response
print(response.choices[0].message.content)