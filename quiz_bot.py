# -*- coding: utf-8 -*-
import sys

import aiml

from nlp import NLP
from BERTnlp import BERTNLP
from util import from_mic, response_agent, read_from_file
from constants import NAME_FILE, TOPIC_FILE

kern = aiml.Kernel()
kern.setTextEncoding(None)
kern.bootstrap(learnFiles="quiz-bot.xml")

nlp = None

if (len(sys.argv) >= 2 and sys.argv[1].lower().strip() == "bert"):
    print("Loading BERT NLP")
    nlp = BERTNLP()
else:
    print("Loading standard NLP")
    nlp = NLP()

# Set any previously mentioned data back into aiml
name = read_from_file(NAME_FILE).strip()
fav_topic = read_from_file(TOPIC_FILE).strip()

if name != "":
    kern.respond("my name is " + name)

if fav_topic != "":
    kern.respond("my favourite topic is " + fav_topic)


print("")
print("=======================================")
print("Hello, my name is quizo the quiz bot !")
print("I am here to serve your quiz needs")
print("HINT: Type in 'voice' to use voice recongnition")
print("=======================================")
print("")

while True:
    try:
        user_input = input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print("Bye!")
        break

    voice = False
    if user_input.lower().strip() == "voice":
        user_input = from_mic()
        print("> " + user_input)
        voice = True

    answer = kern.respond(user_input)
    response = response_agent(answer, nlp, voice)
    voice = False

    if (response == "quit"):
        break

