import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from nlp.nlp import NLP

class BERTNLP():
    def __init__(self):
        self._dataset = NLP.init_data()
        self._dataset = NLP.clean_data(self._dataset)

        self._model = SentenceTransformer('bert-base-nli-mean-tokens')
        self._sentence_embeddings = self._model.encode(tuple(self._dataset['Question']))
    
    def response(self, user_input):
        user_input_embedding = self._model.encode([user_input])
        similarity_array = cosine_similarity(user_input_embedding, self._sentence_embeddings)
        max_similarity = np.argmax(similarity_array, axis=None)

        return self._dataset.iloc[max_similarity]['Answer']
