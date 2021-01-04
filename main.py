#!/usr/bin/python3

# importing needed modules
import re
import random

# importing learned dataset from data.py file
from data import data

# this function reduces copy-pasting
def print_answer(string):
    print("Assistant:", string.strip())

def remove_syntax(string):
    return re.sub("[,.!?\"']*", "", string)

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
                    about_themselves = True

            # if user's input is not a greeting or a question or a statement about themselves/their feelings
            if not about_themselves:
                statement = True

    if user_input == "show me your knowledge":
        print_answer(str(data))

    elif user_input_without_syntax in data["exit"]:
        exit(data)

    # if user's input is a question
    elif question:
        print("This is a question")
        if words[-1] == "mean":
            search_result = ""

            answered = False

            for category in data:
                if words[-2] in data[category]:
                    print_answer(words[-2] + " means " + category)
                    answered = True
                    break
            if not answered:
                print_answer("Sorry, I don't know that. But you can teach me.")

    # if user's input is not a question but a greeting
    elif greeting:
        print("This is a greeting")
        # creating a copy of data["greeting"] list
        greetings = data["greeting"].copy()
        # removing the words that we don't need
        greetings.remove(greeting_word)

        # responding to the user

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

    # if user's input is not a question nor a greeting but it is a statement about themselves
    elif about_themselves:
        print("This is a statement about themselves")
        pass

    # if user's input is not a question nor a greeting nor a statement about themselves but a statement
    elif statement:
        print("This is a statement")
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
            length = len("means") if means else len("is")
            category = user_input_without_syntax[index+length:].strip()
            # if category already exists
            if category in data:
                # append the word to the category
                data[category].append(to_remember)
            # if category does not exist
            else:
                # create it and append to it the word
                data[category] = [to_remember]

    # if the type of user's input is not recognized
    else:
        print("bananas")