import requests
import csv
from bs4 import BeautifulSoup

def get_visible_text(url):
    try:
        response = requests.get(url, timeout=7)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            return text
        else:
            return f"Failed to fetch the content from {url}. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Error: {e}"

def scrape_articles(input_file, output_file):
    # Replace 'urls.csv' with the path to your CSV file containing URLs
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['url', 'text']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, escapechar='\n')
        writer.writeheader()
        for row in reader:
            website_url = row['urls']
            print(f"extracting {website_url}")
            website_text = get_visible_text(website_url)
            if (len(website_text) < 300): #not a useful article/there was an error
                website_text = ""
                print(website_text)
                print("did not add article")
                continue
            writer.writerow({'url': website_url, 'text': website_text})
            print(f"article {website_url} text extracted")