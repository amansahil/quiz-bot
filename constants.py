
import os
from dotenv import load_dotenv

# Load enviroment variables into `os`
load_dotenv()

AZURE_API_KEY = os.getenv('API_KEY')

CATEGORIES = {
   "general knowledge":9,
   "gk":9,
   "books":10,
   "film":11,
   "films":11,
   "movies":11,
   "music":12,
   "musicals & theatres":13,
   "musicals and theatres":13,
   "musicals":13,
   "theathres":13,
   "television":14,
   "tv":14,
   "video games":15,
   "board games":16,
   "games": 16,
   "science & nature":17,
   "science and nature":17,
   "science":17,
   "nature":17,
   "computers":18,
   "mathematics":19,
   "math":19,
   "maths":19,
   "maths":19,
   "mythology":20,
   "sports":21,
   "geography":22,
   "history":23,
   "politics":24,
   "art":25,
   "celebrities":26,
   "animals":27,
   "vehicles":28,
   "comics":29,
   "comic books":29,
   "gadgets":30,
   "anime & manga":31,
   "anime and manga":31,
   "anime":31,
   "manga":31,
   "cartoon & animations":32,
   "cartoon":32,
   "cartoons":32,
   "animation":32,
   "animations":32
}

DIFFICULTIES = { 
    'easy': 'easy', 
    'simple': 'easy', 
    'medium': 'medium', 
    'hard': 'hard',
}

NAME_FILE = 'database/.name'
TOPIC_FILE = 'database/.topic'
KB = 'kb/map-kb.txt'
KB_CACHE = 'kb/kb-cache'
DATASET_1 = 'dataset/dataset-1.txt'
DATASET_2 = 'dataset/dataset-2.txt'
DATASET_3 = 'dataset/dataset-3.txt'
