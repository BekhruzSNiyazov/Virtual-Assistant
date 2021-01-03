#!/usr/bin/python3

# importing needed modules
import re
import random

# importing learned dataset from data.py file
from data import data

# this function reduces copy-pasting
def print_answer(string):
    print("Assistant:", string.strip())

# chatting with user forever until they type "exit" or
# another word in "exit" category
while True:

    # getting an input from the user and removing white spaces
    user_input = input("User: ").strip()

    # creating a variable that stores user's input without useless syntax and lowercased and without white spaces
    user_input_without_syntax = re.sub("[,.!?\"']*", "", user_input).lower().strip()

    # splitting user's input into seperate words
    words = user_input_without_syntax.split()

    # creating variables that will hold information about user's input
    question = False
    greeting = False
    about_themselves = False
    statement = False

    # initializing variables that may become useful in the future
    greeting_word = ""

    # checking if user's input is a greeting
    if user_input_without_syntax in data["greeting"]:
        greeting = True
        greeting_word = user_input_without_syntax

    if not greeting:
        for word in words:
            if word in data["greeting"]:
                greeting = True
                greeting_word = word

    
    # if user's input is not a question
    if not greeting:
        
        # if the last character in user's input is "?"
        if user_input[-1] == "?":
            question = True
        
        # if user's input is not a question
        if not question:

            # checking, if user is saying something about themselves/their feelings
            for word in words:
                if word in data["self"]:
                    about_themselves = True

            # if user's input is not a greeting or a question or a statement about themselves/their feelings
            if not about_themselves:
                statement = True

    # if user's input is a question
    if question:
        pass

    elif greeting:
        # removing the words that we don't need
        greetings = data["greeting"].copy()
        greetings.remove(greeting_word)

        # responding to the user
        if greeting_word == "whats up":
            responses = ["Nothing", "Not much", "Alright"]
            print_answer(random.choice(responses))

        elif greeting_word == "how are you" or greeting_word == "how do you do" or greeting_word == "how are you doing":
            response = random.choice(["Everything is ", "I feel "])

            available_words = data["good"].copy()
            available_words.remove("well")
            available_words.remove("outstanding")
            available_words.remove("terrific")

            response += random.choice(available_words)

            print_answer(response)

    elif about_themselves:
        pass

    elif statement:
        pass

    else:
        print("bananas")