#!/usr/bin/python3

# importing needed modules
import re
import random

# importing learned dataset from data.py file
from data import data

# this function reduces copy-pasting
def print_answer(string):
    print("Assistant: ", string)

# chatting with user forever until they type "exit" or
# another word in "exit" category
while True:

    # getting an input from the user and removing white spaces
    user_input = input("User: ").strip()

    # creating a variable that stores user's input without useless syntax
    user_input_without_syntax = re.sub("[,.!?\"']*", "", user_input)

    # splitting user's input into seperate words
    words = user_input.split()

    # creating variables that will hold information about user's input
    about_themselves = False
    greeting = False
    question = False

    # if the last character in user's input is "?"
    if user_input[-1] == "?":
        question = True
    
    # if user's input is not a question
    if not question:
        pass