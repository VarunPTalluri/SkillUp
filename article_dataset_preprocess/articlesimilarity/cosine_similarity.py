import articlesimilarity.mongodbpull as dbpull
import numpy as np
from numpy.linalg import norm

def get_similarity_between_articles(this_embedding, id):
    other_embeddings = dbpull.get_other_articles_embeddings(id)

    cosine_similarities = {}

    for id, other_embedding in other_embeddings.items():
        cosine = get_similarity_between_embeddings(other_embedding, this_embedding)
        cosine_similarities[id] = cosine
    
    return cosine_similarities

def get_similarity_between_embeddings(a, b):
    return np.dot(a, b)/(norm(a)*norm(b))