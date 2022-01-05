# -*- coding: utf-8 -*-
import aiml
from constants import NAME_FILE, TOPIC_FILE

from util import response_agent, read_from_file

kern = aiml.Kernel()
kern.setTextEncoding(None)
kern.bootstrap(learnFiles="quiz-bot.xml")

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
        userInput = input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print("Bye!")
        break

    answer = kern.respond(userInput)
    response = response_agent(answer)

    if (response == "quit"):
        break

