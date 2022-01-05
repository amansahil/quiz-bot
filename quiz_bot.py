# -*- coding: utf-8 -*-
import aiml

from util import response_agent

kern = aiml.Kernel()
kern.setTextEncoding(None)

kern.bootstrap(learnFiles="quiz-bot.xml")

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

