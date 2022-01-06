import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class BERTNLP():
    def __init__(self):
        d1 = pd.read_csv('./dataset/dataset-1.txt', sep='\t')
        d2 = pd.read_csv('./dataset/dataset-2.txt', sep='\t')
        d3 = pd.read_csv('./dataset/dataset-3.txt', sep='\t', encoding = 'ISO-8859-1')
        
        self._dataset = d1.append([d2, d3])

        self._dataset['Question'] = self._dataset['ArticleTitle'].str.replace('_', ' ') + ' ' + self._dataset['Question']
        self._dataset = self._dataset[['Question', 'Answer']]

        self._dataset = self._clean_data(self._dataset)

        self._model = SentenceTransformer('bert-base-nli-mean-tokens')
        self._sentence_embeddings = self._model.encode(tuple(self._dataset['Question']))
    
    def response(self, user_input):
        user_input_embedding = self._model.encode([user_input])
        similarity_array = cosine_similarity(user_input_embedding, self._sentence_embeddings)
        max_similarity = np.argmax(similarity_array, axis=None)

        return self._dataset.iloc[max_similarity]['Answer']

    def _clean_data(self, data):
        data = data.drop_duplicates(subset='Question')
        data = data.dropna()

        return data
