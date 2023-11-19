import pymongo

mongo_uri = 'mongodb+srv://var123un:123@cluster1.bctyasc.mongodb.net/?retryWrites=true&w=majority'
collection_name = "Collection1"

# Establish a connection to MongoDB
client = pymongo.MongoClient(mongo_uri)

# Access the database and collection
db = client["Database1"]
collection = db[collection_name]
result = collection.find({})

for document in result:
    print(document)  # Process or access each document as needed

client.close()

# Query to pull data (replace with your own query)
"""def get_other_articles(id):

    # Fetch data from the collection
    result = collection.find({})

    documents_list = list(result)
    print(documents_list)  
get_other_articles(0)"""