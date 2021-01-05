#!/usr/bin/python3

# importing needed modules
import re
import random

from googlesearch import search as gSearch

import requests

import wikipedia
from PyDictionary import PyDictionary

# importing learned dataset from data.py file
from data import data

dictionary = PyDictionary()

# this function reduces copy-pasting
def print_answer(string):
    print("Assistant:", string.strip())

def remove_syntax(string):
    return re.sub("[,.!?\"']*", "", string)

def search(search_item, person):
    if person:
        try:
            print_answer("Here is what I found on Wikipedia:")
            print_answer(wikipedia.summary(search_item))
        except:
            try:
                print_answer("Here is what I found on Wikipedia:")
                print_answer(wikipedia.summary(search_item.split()[-1]))
            except:
                try:
                    print_answer("Here is what I found on Wikipedia:")
                    print_answer(wikipedia.summary(search_item.split()[0]))
                except:
                    print_answer("Sorry, I don't know that.")
    else:
        answered = False
        try:
            print_answer("Here are some definitions that I found: ")
            definition = dictionary.meaning(search_item)
            for part in definition:
                print("\t" + part + ":")
                for meaning in definition[part]:
                    print("\t\t" + str(definition[part].index(meaning)+1) + ". " + meaning)
            answered = True
        except:
            for category in data:
                if search_item in data[category]:
                    print_answer(search_item + " is a " + category if search_item != category else search_item + " means " + random.choice(data[category]))
                    answered = True
        if not answered:
            print_answer("Sorry, I don't know that yet. But you can teach me.")

# chatting with user forever until they type "exit" or
# another word in "exit" category
while True:

    # getting an input from the user and removing white spaces
    user_input = input("User: ").strip()

    # creating a variable that stores user's input without useless syntax and lowercased and without white spaces
    user_input_without_syntax = remove_syntax(user_input).lower().strip()

    # splitting user's input into seperate words
    words = user_input_without_syntax.split()

    # creating variables that will hold information about user's input
    question = False
    greeting = False
    about_themselves = False
    statement = False

    # initializing variables that may become useful in the future
    greeting_word = ""
    greetings = [remove_syntax(greeting.lower()) for greeting in data["greeting"]]

    # checking if user's input is a greeting
    if user_input_without_syntax in greetings:
        greeting = True
        greeting_word = data["greeting"][greetings.index(user_input_without_syntax)]

    # if user's input was not yet recognized as a greeting
    if not greeting:
        for word in words:
            if word in greetings:
                greeting = True
                greeting_word = data["greeting"][greetings.index(word)]

    # if user's input is not a greeting
    if not greeting:
        
        if len(user_input) > 1:
            # if the last character in user's input is "?"
            if user_input[-1] == "?" or user_input[-2] == "?" or user_input[-3] == "?":
                question = True

        # if user's input was not yet recognized as a question
        if not question:
            if words[0].capitalize() in data["question_keywords"]:
                question = True
        
        # if user's input is not a question
        if not question:

            # checking, if user is saying something about themselves/their feelings
            for word in words:
                if word in data["self"]:
                    if word == "my":
                        if "is" in words: statement = True
                    about_themselves = True

            # if user's input is not a greeting or a question or a statement about themselves/their feelings
            if not about_themselves:
                statement = True

    if user_input == "show me your knowledge":
        print_answer(str(data))

    elif user_input_without_syntax in data["exit"]:
        exit(data)

    # if user's input is a question
    if question:
        if words[-1] == "mean":
            search_result = ""

            search_item = user_input_without_syntax[user_input_without_syntax.index("does") + len("does") + 1 : user_input_without_syntax.index("mean")].strip()

            search(search_item, False)
        else:
            if re.match(r"what is [\w\s]+", user_input_without_syntax) or re.match(r"who is [\w\s]+", user_input_without_syntax):
                search_item = user_input_without_syntax[len(words[0]) + len(words[1]) + 2:].strip()
                search(search_item, False if words[0] == "what" else True)

    # if user's input is a greeting
    if greeting:
        # creating a copy of data["greeting"] list
        greetings = data["greeting"].copy()
        # removing the words that we don't need
        greetings.remove(greeting_word)

        # answering to the user

        # if user asked "what's up?"
        if greeting_word == "What's up?":
            responses = ["Nothing", "Not much", "Alright"]
            print_answer(random.choice(responses))

        # if user did not ask "what's up?" but they asked "how are you" or "how do you do" or "how are you doing"
        elif greeting_word == "How are you?" or greeting_word == "How do you do?" or greeting_word == "How are you doing?":

            # creating a response variable with a start; one word will be appended to it
            response = random.choice(["Everything is ", "I feel "])

            # creating a copy of data["good"] list
            available_words = data["good"].copy()

            # filtering the list from unwanted words
            available_words.remove("well")
            available_words.remove("outstanding")
            available_words.remove("terrific")
            available_words.remove("exceptional")
            available_words.append("really well")

            # appending a word to the response
            response += random.choice(available_words)

            # answering to the user
            print_answer(response)

        # if user did not ask "what's up?" nor "how are you" or "how do you do" or "how are you doing"
        else:
            # creating a copy of data["greeting"] list
            greetings = data["greeting"].copy()

            # filtering the list
            greetings.remove(greeting_word)

            # answering to the user
            print_answer(random.choice(greetings))

    # if user's input is a statement about themselves
    if about_themselves:
        pass

    # if user's input is a statement
    if statement:
        # creating variables that will hold information about user's input
        explanation = False

        # initializing variables that will be useful in the future
        means = False

        if "means" in words:
            explanation = True
            means = True
        elif "is" in words:
            if words[words.index("is")+1] == "a" or words[words.index("is")+1] == "an":
                explanation = True
        else:
            print_answer("Sorry, but I don't understand you.")

        # if user's input is an explanation:
        if explanation:
            index = user_input_without_syntax.index("means") if means else user_input_without_syntax.index("is")
            to_remember = user_input_without_syntax[:index].strip()
            length = len("means") if means else len("is") + len(words[words.index("is")+1]) + 1
            category = user_input_without_syntax[index+length:].strip()
            # if category already exists
            if category in data:
                # append the word to the category
                data[category].append(to_remember)
            # if category does not exist
            else:
                # create it and append to it the word
                data[category] = [to_remember]