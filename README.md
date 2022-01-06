# QUIZ BOT

A chat bot for all your quiz needs integrated with azure voice services.ß1

## Setup

### Install

Requires python 3.6 or above

    pip install -r requirements.txt

Install nltkfiles

    python
1
    >>> import nltk
    >>> nltk.download('omw-1.4')
    >>> nltk.download('wordnet')
    >>> nltk.download('stopwords')
    >>> nltk.download('punkt')
    >>> nltk.download('averaged_perceptron_tagger')

### Enviroment variables

Create a `.env` file with your azure your voice service API key

    API_KEY=<YOUR-AZURE-API-KEY>

## Run

Use standard NLP:

    python quiz_bot.py


Use BERT NLP:

    python quiz_bot.py bert

**Note** : For the BERT NLP command you might need to prepend sudo to it, as pytorch requires some admin priviliges 
