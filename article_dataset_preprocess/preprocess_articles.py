from articles_scraper import scrape_articles
from article_cleaner import clean_article_text
from summarizer import create_summaries_for_articles
from upload_data_to_mongodbatlas import upload_to_mongodb, reset_db, insert_articles_to_mongodb, mass_upload
from embeddings.embeddings import get_embeddings_csv
#from add_articles_to_rails_db import build_db
reset_db()
#scrape_articles('urls2.csv', 'extracted_text.csv')
#clean_article_text('extracted_text.csv', 'cleaned_extracted_text.csv')
#create_summaries_for_articles('cleaned_extracted_text.csv', 'articles_w_summaries.csv')
#upload_to_mongodb('cleaned_extracted_text.csv')
embeddings = get_embeddings_csv('cleaned_extracted_text.csv')
mass_upload(embeddings)
#build_db('urls.csv')
