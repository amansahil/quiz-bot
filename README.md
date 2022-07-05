# QUIZ BOT

A chatbot for all your quiz needs especially vexillology. Integrted with Azure AI services and image classification.

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

### Image classifier

Export the h5 file for the image classifier by running the notebook in the CNN-Notebook folder. Copy the generated h5 file into the root directory

### Enviroment variables

Create a `.env` file with your relevant azure keys

    API_KEY=<YOUR-AZURE-API-VOICE-KEY>

    PROJECT_ID=<PROJECT-ID>
    CV_KEY=<CV-KEY>
    CV_ENDPOINT=<CV-ENDPOINT>
    MODEL_NAME=<MODEL-NAME>

    COG_KEY=<COG-KEY>
    COG_ENDPOINT=<COG-ENDPOINT>
    COG_REGION=<COG-REGION>

## Run

Use standard NLP:

    python quiz_bot.py

Use BERT NLP:

    python quiz_bot.py bert

**Note** : For the BERT NLP command, you might need to prepend `sudo` to it, as PyTorch requires some admin privileges 

**Note 2** : Delete the `kb-cache` file if you want to load the knowledge base from `map-kb.txt` instead

## Example chats

### Conversation 1 (Simple)

    > Hello

    Would you like a quick quiz question ?

    > yes

    Ellie Goulding's earliest album was named?

    1) Lights
    2) Halcyon Days
    3) Bright Lights
    4) Halcyon

    > halcyon days

    Better luck next time :/, the correct answer was lights

### Conversation 2 (Context & Memory)

    > quiz me on science

    What do you study if you are studying entomology?

    1) Insects
    2) the Brain
    3) Humans
    4) Fish

    > insects

    Correct!!!

    > give me another one

    Approximately how long is a year on Uranus?

    1) 84 Earth years
    2) 109 Earth years
    3) 47 Earth years
    4) 62 Earth years

    > 84 earth years

    Correct!!!

    > give me a fact on my favourite topic

    You have not told me your favourite topic
    > it is anime

    I will remember that :)

    > give me a fact on my favourite topic

    Who is the creator of the manga series "One Piece"?

    Answer: Eiichiro Oda

    > another one on science

    Which of the following mathematicians made major contributions to game theory?

    Answer: John Von Neumann

### Conversation 3 (Quizing)

    > Where was Abraham Lincoln born?    
    
    Hardin County
    
    > Isaac newton birth date
    
    Christmas Day, December 25, 1642.
    
    > Can whales fly?
    
    No
    
    > How tall is a piano?
    
    Studio pianos are around 42 to 45 inches tall.

## Example Image Detection

The chat bot provides a GUI interface to select the images of flags the user wishes to use.

Example queries:

    > What is the flag in this image 
    > What are the flags in this image

Depending on the way the question was asked the chatbot will use either single object detection or multi object detection. 

### Single Object Detection

### Multi Object Detection
