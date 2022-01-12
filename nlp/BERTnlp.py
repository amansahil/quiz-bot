import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from nlp.nlp import NLP
from utils.constants import DATASET_1, DATASET_2, DATASET_3

class BERTNLP():
    def __init__(self):
        d1 = pd.read_csv(DATASET_1, sep='\t')
        d2 = pd.read_csv(DATASET_2, sep='\t')
        d3 = pd.read_csv(DATASET_3, sep='\t', encoding = 'ISO-8859-1')
        
        self._dataset = d1.append([d2, d3])

        self._dataset['Question'] = self._dataset['ArticleTitle'].str.replace('_', ' ') + ' ' + self._dataset['Question']
        self._dataset = self._dataset[['Question', 'Answer']]

        self._dataset = NLP._clean_data(self._dataset)

        self._model = SentenceTransformer('bert-base-nli-mean-tokens')
        self._sentence_embeddings = self._model.encode(tuple(self._dataset['Question']))
    
    def response(self, user_input):
        user_input_embedding = self._model.encode([user_input])
        similarity_array = cosine_similarity(user_input_embedding, self._sentence_embeddings)
        max_similarity = np.argmax(similarity_array, axis=None)

        return self._dataset.iloc[max_similarity]['Answer']

