# -*- coding: utf-8 -*-
import requests, json
import random
import html

from nltk.corpus import wordnet as wn

from constants import CATEGORIES, DIFFICULTIES

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
        print(str(i) + ") " + option)
        i = i + 1 

    userInput = input("> ")
    userInput = userInput.lower().strip()
    if (userInput.isnumeric()):
        if (options[int(userInput) - 1] == results['correct_answer']):
            print("Correct!!!")
            return

    if (userInput == answer):
        print("Correct!!!")
    else:
        print("Better luck next time :/, the correct answer was " + results['correct_answer'])

def _fact(difficulty=None, category=None):

    results = _call_quiz_api(difficulty, category)

    print(html.unescape(results['question']))
    print("")
    print("Answer: " + results['correct_answer'])

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
    if (len(params) == 2 and params[1] != ""):
        category = params[1].lower().strip() 
        if category in CATEGORIES:
            func(category = CATEGORIES[category])
        else:
            print("I don't know any "+message+" on " + params[1])
    elif (len(params) == 3):
        difficulty = params[1].lower().strip() 
        category = params[2].lower().strip() 

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

def response_agent(answer):
    if len(answer) > 0 and answer[0] == '#':
        params = answer[1:].split('$')
        cmd = int(params[0])
        if cmd == 0:
            print(params[1])
            return "quit"
        elif cmd == 1:
            _api_intent_check(params, _quiz, "questions")
        elif cmd == 2:
            _api_intent_check(params, _fact, "facts")
        elif cmd == 99:
            print("I don't know how to respond to that, maybe I will learn one day")
    else:
        print(answer)
