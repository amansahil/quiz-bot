import pandas as pd
import numpy as np
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import data, pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.constants import DATASET_1, DATASET_2, DATASET_3

class NLP:
    def __init__(self):
        d1 = pd.read_csv(DATASET_1, sep='\t')
        d2 = pd.read_csv(DATASET_2, sep='\t')
        d3 = pd.read_csv(DATASET_3, sep='\t', encoding = 'ISO-8859-1')
        
        self._dataset = d1.append([d2, d3])

        self._dataset['Question'] = self._dataset['ArticleTitle'].str.replace('_', ' ') + ' ' + self._dataset['Question']
        self._dataset = self._dataset[['Question', 'Answer']]

        self._dataset = self._clean_data(self._dataset)

        self._tfidf_vectorizer = TfidfVectorizer(tokenizer=self._tokenizer) 
        self._tfidf_matrix = self._tfidf_vectorizer.fit_transform(tuple(self._dataset['Question']))

    def _tokenizer(self, doc):
        stopwords_list = stopwords.words('english')

        lemmatizer = WordNetLemmatizer()

        words = word_tokenize(doc)
        
        pos_tags = pos_tag(words)
        
        non_stopwords = [w for w in pos_tags if not w[0].lower() in stopwords_list]
        
        non_punctuation = [w for w in non_stopwords if not w[0] in string.punctuation]
        
        lemmas = []

        for w in non_punctuation:
            if w[1].startswith('J'):
                pos = wordnet.ADJ
            elif w[1].startswith('V'):
                pos = wordnet.VERB
            elif w[1].startswith('N'):
                pos = wordnet.NOUN
            elif w[1].startswith('R'):
                pos = wordnet.ADV
            else:
                pos = wordnet.NOUN
            
            lemmas.append(lemmatizer.lemmatize(w[0], pos))

        return lemmas

    def response(self, user_input):
        user_input_vector = self._tfidf_vectorizer.transform([user_input])
        similarity_array = cosine_similarity(user_input_vector, self._tfidf_matrix)
        max_similarity = np.argmax(similarity_array, axis=None)

        return self._dataset.iloc[max_similarity]['Answer']

    @staticmethod
    def _clean_data(data):
        data = data.drop_duplicates(subset='Question')
        data = data.dropna()

        return data
