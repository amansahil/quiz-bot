# -*- coding: utf-8 -*-
import os
import requests, json
import random
import html

import azure.cognitiveservices.speech as speechsdk
from nltk.corpus import wordnet as wn

from constants import CATEGORIES, DIFFICULTIES, NAME_FILE, TOPIC_FILE, AZURE_API_KEY

_previous_query = {
    'func': None,
    'category': None,
    'difficulty': None,
    'message': None,
}

_speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region="eastus")


_speech_recognizer = speechsdk.SpeechRecognizer(speech_config=_speech_config)

_speech_config.speech_synthesis_language = "en-GB"
_speech_config.speech_synthesis_voice_name ="en-GB-SoniaNeural"
_audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
_synthesizer = speechsdk.SpeechSynthesizer(speech_config=_speech_config, audio_config=_audio_config)

def _call_quiz_api(difficulty=None, category=None):

    response = requests.get(
        'https://opentdb.com/api.php',
        params = {
            "amount": 1,
            "type": "multiple",
            "difficulty": difficulty,
            "category": category
        }
    )                

    return json.loads(response.content)['results'][0]

def _quiz(difficulty=None, category=None):

    results = _call_quiz_api(difficulty, category)
    answer = results['correct_answer'].lower().strip()

    options = results['incorrect_answers']
    options.append(results['correct_answer'])
    random.shuffle(options)

    print(html.unescape(results['question']))
    print("")

    i = 1
    for option in options:
        print(html.unescape(str(i) + ") " + option))
        i = i + 1 

    user_input = input("> ")
    user_input = user_input.lower().strip()
    if (user_input.isnumeric()):
        if (options[int(user_input) - 1] == results['correct_answer']):
            print("Correct!!!")
            return

    if (user_input == answer):
        print("Correct!!!")
    else:
        print("Better luck next time :/, the correct answer was " + results['correct_answer'])

def _fact(difficulty=None, category=None):

    results = _call_quiz_api(difficulty, category)

    print(html.unescape(results['question']))
    print("")
    print(html.unescape("Answer: " + results['correct_answer']))

def _synonym_check(word, dict, pos=wn.ADJ):
    net = wn.synsets(word, pos=pos)
    if len(net) == 0:
        return None
    
    syn_word = net[0]

    for key in dict.keys():
        net_to_compare = wn.synsets(key, pos=pos)
        if len(net_to_compare) == 0:
            continue

        syn_to_compare = wn.synsets(key, pos=pos)[0]
        score = syn_to_compare.path_similarity(syn_word)

        if(score == 1.0):
            return key

    return None

def _api_intent_check(params, func, message):

    _previous_query['func'] = func
    _previous_query['message'] = message

    if (len(params) == 2 and params[1] != ""):
        category = params[1].lower().strip() 

        _previous_query['category'] = category

        if category in CATEGORIES:
            func(category = CATEGORIES[category])
        else:
            print("I don't know any "+message+" on " + params[1])
    elif (len(params) == 3):
        difficulty = params[1].lower().strip() 
        category = params[2].lower().strip() 

        _previous_query['category'] = category
        _previous_query['difficulty'] = difficulty

        if category not in CATEGORIES:
            category = _synonym_check(category, CATEGORIES)        

            if category is None:
                print("I don't know any "+message+" on " + params[2])
                return
        elif difficulty not in DIFFICULTIES:
            synonym = _synonym_check(difficulty, DIFFICULTIES)        

            if synonym is not None:
                func(difficulty=DIFFICULTIES[synonym], category=CATEGORIES[category])
            else:
                print("I don't know any "+difficulty+" " +message)
                return
        else:        
            func(difficulty=DIFFICULTIES[difficulty], category=CATEGORIES[category])
    else:
        func()

def _write_to_file(file_name, content):
    f = open(os.path.join(os.getcwd(), file_name), 'w')
    f.write(content)
    f.close()

def read_from_file(file_name):
    path = os.path.join(os.getcwd(), file_name)
    if os.path.isfile(path):
        f = open(path, 'r')
        return f.readline()
    
    return ""

def response_agent(answer, nlp, voice=False):
    if len(answer) > 0 and answer[0] == '#':
        params = answer[1:].split('$')
        cmd = int(params[0])
        if cmd == 0:
            respond(params[1], voice)
            return "quit"
        elif cmd == 1:
            if voice:
                respond("Sure ! One sec.", voice, display=False)

            _api_intent_check(params, _quiz, "questions")
        elif cmd == 2:
            if voice:
                respond("Sure ! One sec", voice, display=False)

            _api_intent_check(params, _fact, "facts")
        elif cmd == 3:            
            _write_to_file(NAME_FILE, params[1])
            respond("Nice to meet you " + params[1], voice)
        elif cmd == 4:
            _write_to_file(TOPIC_FILE, params[1])
            respond("I will remember that :)", voice)
        elif cmd == 5:
            if _previous_query["func"] is None:
                return respond("Another what ?", voice)                

            category = params[1] if (len(params) >= 2 and params[1] != "") else _previous_query["category"] 
            difficulty = params[2] if (len(params) >= 3 and params[2] != "") else _previous_query["difficulty"]  

            params = ['']

            if category is not None:
                params.append(category)
            
            if difficulty is not None:
                params.append(difficulty)
            
            _api_intent_check(params, _previous_query["func"], _previous_query["message"])
        elif cmd == 99:
            user_input = params[1].strip()
            respond(nlp.response(user_input), voice)
    else:
        respond(answer, voice)

def from_mic():
    print("Speak into your microphone : ")
    result = _speech_recognizer.recognize_once_async().get()
    return result.text

def respond(text, voice=False, display=True):
    if voice:
        if display:
            print(text)

        _synthesizer.speak_text_async(text)
    else:
        print(text)