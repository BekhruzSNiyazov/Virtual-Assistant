#!/usr/bin/python3

# importing needed modules
import re
import random

from googlesearch import search as gSearch

import wikipedia
from PyDictionary import PyDictionary

from datetime import datetime

# importing dataset from data.py file
from data import data

dictionary = PyDictionary()

last_assistant = ""

# this function reduces copy-pasting
def print_answer(string):
	print("\nAssistant:", string)

def remove_syntax(string):
	return re.sub("[,.!?\"']*", "", string)

def search(search_item, person):
	if person:
		try:
			answer = search_wikipedia(search_item)
			found_on_wikipedia()
			print_answer(answer)
		except:
			try:
				answer = search_wikipedia(search_item.split()[-1])
				found_on_wikipedia()
				print_answer(answer)
			except:
				try:
					answer = search_wikipedia(search_item.split()[0])
					found_on_wikipedia()
					print_answer(answer)
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

def search_wikipedia(search_item):
	return wikipedia.summary(search_item)

def found_on_wikipedia():
	print_answer("Here is what I found on Wikipedia:")

# chatting with user forever until they type "exit" or
# another word in "exit" category
while True:

	# getting an input from the user and removing white spaces
	user_input = input("\nUser: ").strip()

	# creating a variable that stores user's input without useless syntax and lowercased and without white spaces
	user_input_without_syntax = remove_syntax(user_input).lower().strip()

	# splitting user's input into seperate words
	words = user_input_without_syntax.split()

	# creating variables that will hold information about user's input
	question = False
	greeting = False
	about_themselves = False
	statement = False
	about_it = False

	# initializing variables that may become useful in the future
	greeting_word = ""
	greetings = [remove_syntax(grtng.lower()) for grtng in data["greeting"]]

	# checking if user's input is a greeting
	if user_input_without_syntax in greetings:
		greeting_word = data["greeting"][greetings.index(user_input_without_syntax)]
		greeting = True

	# if user's input wasn't yet recognized as a greeting
	if not greeting:
		if len(words) > 1:
			if words[1] in data["greeting"]:
				greeting_word = words[1]
				greeting = True

	# last check
	if not greeting:
		for grtng in data["greeting"]:
			if user_input_without_syntax.startswith(remove_syntax(grtng).lower()):
				greeting_word = grtng
				greeting = True
				break
			elif user_input_without_syntax.endswith(remove_syntax(grtng).lower()):
				greeting_word = grtng
				greeting = True

	# if user's input is not a greeting
	if not greeting:
		
		if len(user_input) > 3:
			for word in data["self"]:
				if word in words:
					if word == "youre" or "are" in words:
						about_it = True
						break

			if not about_it:
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
						if word in data["themselves"]:
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
		print("This is a question")
		if re.match(r"what does [\w\s]+ mean", user_input_without_syntax):

			search_item = user_input_without_syntax[user_input_without_syntax.index("does") + len("does") + 1 : user_input_without_syntax.index("mean")].strip()

			search(search_item, False)
		else:
			if re.match(r"what is [\w\s]+", user_input_without_syntax) or re.match(r"who is [\w\s]+", user_input_without_syntax):
				search_item = user_input_without_syntax[len(words[0]) + len(words[1]) + 2:].strip()
				search(search_item, False if words[0] == "what" else True)

	# if user said something about assistant
	if about_it:
		print("They said something about assistant")
		
		for word in words:
			if word in data["good"]:
				print_answer("Thanks a ton!")
			elif word in data["bad"]:
				print_answer("Please, contact @bekhruzniyazov on Tim's Discord and tell him the reason why you didn't like me. :(")

	# if user's input is a greeting
	if greeting:
		print("This is a greeting")
		
		answered = False

		hour = datetime.now().time().hour

		if greeting_word == "Good morning!" or greeting_word == "Morning":
			if hour > 12:
				if hour < 17:
					print_answer("It is no longer morning, I believe. It is already afternoon.")
					answered = True
				elif hour < 20:
					print_answer("It is evening now. Good evening to you!")
					answered = True
				else:
					print_answer("Good night. It's night now.")
					answered = True
			else:
				print_answer("Good morning!")
				answered = True

		elif greeting_word == "Good day!" or greeting_word == "Day":
			if hour < 12 or hour > 17:
				if hour < 12:
					print_answer("It is only morning yet, I believe. Good morning to you!")
					answered = True
				elif hour > 17:
					print_answer("It is evening now.")
					answered = True
				elif hour > 20:
					print_answer("Good night. It is night now.")
					answered = True
			else:
				print_answer("Good day!")
				answered = True

		elif greeting_word == "Good evening" or greeting_word == "Evening":
			if hour < 17 or hour > 20:
				if hour < 12:
					print_answer("It is only morning now. Good morning!")
				elif hour < 17:
					print_answer("It is not evening yet. Good day to you!")
					answered = True
				elif hour > 20:
					print_answer("It is night now. Good night to you!")
					answered = True
			else:
				print_answer("Good evening!")
				answered = True

		elif greeting_word == "Good night!" or greeting_word == "Night":
			if hour < 20 or hour > 6:
				if hour < 20:
					print_answer("It is not night yet.")
					answered = True
				elif hour > 6:
					print_answer("It is no longer night.")
					answered = True
			else:
				print_answer("Good night to you!")
				answered = True

		if not answered:
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
				available_words.remove("fine")
				available_words.remove("cool")
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
				words = ["Hullo", "Sup", "Hulo", "Day", "Morning", "Evening", "Night", "Good morning!", "Good day!", "Good evening!", "Good night!"]
				if greeting_word not in words: greetings.remove(greeting_word)
				for word in words:
					greetings.remove(word)

				# answering to the user
				print_answer(random.choice(greetings))

	# if user's input is a statement about themselves
	if about_themselves:

		print("This is a statement about themselves")
		
		if re.match(r"i feel [\w\s]+[,]*[\w\s]*", user_input_without_syntax):

			their_feelings = re.findall(r"i feel ([\w\s]+)", user_input_without_syntax)[0]

			answered = False

			for word in their_feelings.split():

				word = word.strip()
				
				if word in data["good"]:
					print_answer(":-)")
					answered = True
					break
				
				elif word in data["bad"]:
					print_answer("Can I cheer you up somehow? You can ask me for a joke.")
					answered = True
					break

			if not answered:
				print_answer("Sorry, but I don't know what \"" + their_feelings + "\" means.")

		if re.match(r"i am a[n]* [\w\s]+", user_input_without_syntax):

			answered = False

			noun = re.findall(r"i am a[n]* ([\w\s]+)", user_input_without_syntax)[0]

			for word in noun.split():

				word = word.strip()

				if word in data["good"]:
					print_answer("I agree with you.")
					answered = True
					break

				elif word in data["bad"]:
					print_answer("I feel so sorry about that. Can I help you somehow?")
					answered = True
					break

			if not answered:
				print_answer("I am sorry, but I do not know what \"" + noun + "\" means.")

	# if user's input is a statement
	if statement:
		
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