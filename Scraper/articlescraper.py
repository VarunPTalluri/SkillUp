import requests
import csv
from bs4 import BeautifulSoup

def get_visible_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            return text
        else:
            return f"Failed to fetch the content from {url}. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Error: {e}"

# Replace 'urls.csv' with the path to your CSV file containing URLs
input_csv_file = 'Scraper/urls.csv'
output_csv_file = 'Scraper/extracted_text.csv'  # Replace with the desired output file name

with open(input_csv_file, 'r') as infile, open(output_csv_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['url', 'text']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        website_url = row['urls']
        website_text = get_visible_text(website_url)
        writer.writerow({'url': website_url, 'text': website_text})