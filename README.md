# Setup

Requires python 3.6 or above

    pip install -r requirements.txt

Install wordnet and stopwords from nltk

    python
    >>> import nltk
    >>> nltk.download('wordnet')
    >>> nltk.download('stopwords')
    >>> nltk.download('punkt')
    >>> nltk.download('averaged_perceptron_tagger')