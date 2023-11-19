import pandas as pd
import pymongo

def upload_to_mongodb(input_file):
    id_number = 0

    # Set your MongoDB Atlas connection string
    mongo_uri = 'mongodb+srv://var123un:123@cluster1.bctyasc.mongodb.net/?retryWrites=true&w=majority'

    # Connect to MongoDB Atlas
    client = pymongo.MongoClient(mongo_uri)

    # Replace 'your_database' and 'your_collection' with your actual database and collection names
    db = client['Database1']
    collection = db['Collection1']
    # Clear the collection before inserting new data
    collection.delete_many({})

    # Read CSV file into a pandas DataFrame
    data = pd.read_csv(input_file)

    # Convert DataFrame to a list of dictionaries (each row becomes a dictionary)
    data_dict = data.to_dict(orient='records')

    collection.create_index([("id_number", pymongo.ASCENDING)])
 
    # Insert each record into MongoDB
    for record in data_dict:
        # Optional: You can add additional preprocessing or transformation here if needed
        # For example, you may want to convert data types or perform other manipulations

        # Set the custom _id value
        record['_id'] = id_number
        
        # Insert the record into MongoDB
        inserted_record = collection.insert_one(record)
        
        print(f"Inserted record with _id: {id_number}")
        id_number += 1

    # Close the MongoDB connection
    client.close()


upload_to_mongodb('cleaned_extracted_text.csv')