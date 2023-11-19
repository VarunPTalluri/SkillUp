import psycopg2
import os
from tqdm import tqdm
import pandas as pd
import datetime

def add_article(cursor, title, url, current_time):
    sql = """
    INSERT INTO articles (title, url, created_at, updated_at) VALUES 
    (%s, %s, %s, %s) RETURNING id;
    """
    cursor.execute(sql, (title, url, current_time, current_time))


def build_db(input_file):
    # Database credentials
    db_host = '127.0.0.1'
    db_port = 5432
    db_name = 'skillup_db'
    db_user = 'apple'
    db_password = 'aaa'

    # Connect to the PostgreSQL database
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        cursor = connection.cursor()
        print('Connected to PostgreSQL!')

        indf = pd.read_csv(input_file)

        for i, row in indf.iterrows():
            current_time = '2023-11-19 02:06:28'
            add_article(cursor, row['headline'], row['urls'], current_time)

        connection.commit()
        print('Successfully Updated Database')

    except (Exception, psycopg2.Error) as error:
        print('Error with PostgreSQL:', error)

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()
            print('Closed PostgreSQL Connection')
