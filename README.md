# QUIZ BOT

A chatbot for all your quiz needs, integrated with azure voice services

## Setup

### Install

Requires python 3.6 or above

    pip install -r requirements.txt

Install nltkfiles

    python

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

**Note** : For the BERT NLP command, you might need to prepend `sudo` to it, as PyTorch requires some admin privileges 

**Note 2** : Delete the `kb-cache` file if you want to load the knowledge base from `map-kb.txt` instead
