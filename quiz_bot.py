# -*- coding: utf-8 -*-
import aiml
from constants import NAME_FILE, TOPIC_FILE

from nlp import NLP
from util import response_agent, read_from_file

kern = aiml.Kernel()
kern.setTextEncoding(None)
kern.bootstrap(learnFiles="quiz-bot.xml")

nlp = NLP()

# Set any previously mentioned data back into aiml
name = read_from_file(NAME_FILE).strip()
fav_topic = read_from_file(TOPIC_FILE).strip()

if name != "":
    kern.respond("my name is " + name)

if fav_topic != "":
    kern.respond("my favourite topic is " + fav_topic)


print("=======================================")
print("Hello, my name is quizo the quiz bot !")
print("I am here to serve your quiz needs")
print("=======================================")

while True:
    try:
        user_input = input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print("Bye!")
        break

    answer = kern.respond(user_input)
    response = response_agent(answer, nlp)

    if (response == "quit"):
        break

