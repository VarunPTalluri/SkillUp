from openai import AzureOpenAI
import numpy as np
import pandas as pd

def create_summaries_for_articles(input_file, output_file):
    with open("SECRETKEY.txt", "r") as f:
        key = f.read()
        key = key.split('\n')[0]

    client = AzureOpenAI(api_key=key,
    azure_endpoint='https://api.umgpt.umich.edu/azure-openai-api/ptu',
    api_version='2023-03-15-preview')

    indf = pd.read_csv(input_file)

    #outdict = {"index": [], "summary": [], "url": []}
    summaries = []

    for index, row in indf.iterrows():

        text = row['text']
        response = client.chat.completions.create(model='gpt-4',
        messages=[
            {"role": "system", "content": "You are a helpful assistant trying to encourage someone to read an article"},
            {"role": "user", "content": "Summarize the text deliminated by the triple quotes, capturing key ideas and themes, in a paragraph\n" + f'"""{text}"""'}
        ])
        final_response = response.choices[0].message.content

        summaries.append(final_response)

        print(f"article {index} done")
    # print the response
    indf.insert(3, "Summary", summaries, True)
    indf.to_csv(output_file)