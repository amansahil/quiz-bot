# Setup

Requires python 3.6 or above

    pip install -r requirements.txt

Install wordnet and stopwords from nltk

    python
    >>> import nltk
    >>> nltk.download('omw-1.4')
    >>> nltk.download('wordnet')
    >>> nltk.download('stopwords')
    >>> nltk.download('punkt')
    >>> nltk.download('averaged_perceptron_tagger')

# Run

Use standard NLP:

    python quiz_bot.py


Use BERT NLP:

    python quiz_bot.py bert

**Note** : You might need to prepend sudo to it, as pytorch required some admin priviliges 
