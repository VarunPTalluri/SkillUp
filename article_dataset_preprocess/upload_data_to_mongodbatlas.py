import pandas as pd
import pymongo
import articlesimilarity.cosine_similarity as co_sim
import articlesimilarity.mongodbpull as dbpull
def reset_db():
    mongo_uri = 'mongodb+srv://var123un:123@cluster1.bctyasc.mongodb.net/?retryWrites=true&w=majority'

    # Connect to MongoDB Atlas
    client = pymongo.MongoClient(mongo_uri)

    # Replace 'your_database' and 'your_collection' with your actual database and collection names
    db = client['Database1']
    collection = db['Collection1']
    print(client)
    # Clear the collection before inserting new data
    collection.delete_many({})
    client.close()
def upload_to_mongodb(input_file):
    id_number = 0

    # Set your MongoDB Atlas connection string
    mongo_uri = 'mongodb+srv://var123un:123@cluster1.bctyasc.mongodb.net/?retryWrites=true&w=majority'

    # Connect to MongoDB Atlas
    client = pymongo.MongoClient(mongo_uri)

    # Replace 'your_database' and 'your_collection' with your actual database and collection names
    db = client['Database1']
    collection = db['Collection1']
    print(client)
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

def mass_upload(embeddings):

    mongo_uri = 'mongodb+srv://var123un:123@cluster1.bctyasc.mongodb.net/?retryWrites=true&w=majority'

    # Connect to MongoDB Atlas
    client = pymongo.MongoClient(mongo_uri)

    # Replace 'your_database' and 'your_collection' with your actual database and collection names
    db = client['Database1']
    collection = db['Collection1']

    total_cosine_similarities = []

    for i in range(len(embeddings)):

        cosine_similarities = []

        for j in range(len(embeddings)):
            if (i != j):
                cosine = co_sim.get_similarity_between_embeddings(embeddings[i], embeddings[j])
                cosine_similarities.append(cosine)
            else:
                cosine_similarities.append(-100)

        total_cosine_similarities.append(cosine_similarities)
        
    dfdict = {"id": [x for x in range(len(embeddings))], "embeddings": embeddings, "similarity_against": total_cosine_similarities}
    df = pd.DataFrame(data=dfdict)

    # Convert DataFrame to a list of dictionaries (each row becomes a dictionary)
    data_dict = df.to_dict(orient='records')

    collection.create_index([("id_number", pymongo.ASCENDING)])
    id_number = 0
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

    return cosine_similarities

def insert_article_to_mongodb(embedding):
    # Set your MongoDB Atlas connection string
    mongo_uri = 'mongodb+srv://var123un:123@cluster1.bctyasc.mongodb.net/?retryWrites=true&w=majority'

    # Connect to MongoDB Atlas
    client = pymongo.MongoClient(mongo_uri)

    # Replace 'your_database' and 'your_collection' with your actual database and collection names
    db = client['Database1']
    collection = db['Collection1']

    #get most recent record
    curr_id = -1
    for result in collection.find().limit(1).sort({"$natural":-1}):
        curr_id = int(result["_id"])

    curr_id += 1

    record = {'_id' : str(curr_id), 'embeddings': embedding, 'similarity_against':[]}

    similarities = co_sim.get_similarity_between_articles(embedding, curr_id)

    record['similarity_against'] = similarities

    #print(record)

    collection.insert_one(record)

    lookedat = [curr_id]
    for i in range(curr_id):
        other_embedding = dbpull.get_this_articles_embeddings(i)
        new_similarity = co_sim.get_similarity_between_embeddings(embedding, other_embedding)
        collection.update_one({'_id': {"$nin": lookedat}}, {'$push': {'similarity_against': new_similarity}}, upsert = True)
        lookedat.append(i)
        
    client.close()

def insert_articles_to_mongodb(embeddings):
    for embedding in embeddings:
        insert_article_to_mongodb(embedding)
