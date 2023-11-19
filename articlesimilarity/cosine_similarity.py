import mongodbpull as dbpull
import numpy as np
from numpy.linalg import norm

def get_similarity_between_articles(id):
    other_embeddings = dbpull.get_other_articles_embeddings(id)
    this_embedding = dbpull.get_this_articles_embeddings(id)

    cosine_similarities = []

    for other_embedding in other_embeddings:
        cosine = np.dot(other_embedding, this_embedding)/(norm(other_embedding)*norm(this_embedding))
        cosine_similarities.append(cosine)
    
    return cosine_similarities
