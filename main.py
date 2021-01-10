#!/usr/bin/python3

# importing needed modules
import re
import random

from googlesearch import search as gSearch

import wikipedia
from PyDictionary import PyDictionary

from datetime import datetime

from gtts import gTTS
from playsound import playsound

import threading

import os

from sys import argv

import time

# importing dataset from data.py file
from data import data

dictionary = PyDictionary()

last_assistant = ""

tts_off = False

word_to_remove = ""

if len(argv) > 1:
	if argv[1] == "--tts-off":
		tts_off = True

def say(string):
	if len(string) < 100:
		tts = gTTS(text=string)
		try:
			filename = "speech" + str(random.randint(0, 100)) + ".mp3"
			tts.save(filename)
			playsound(filename)
			os.system("rm " + filename)
		except Exception as e: print(e)

def print_answer(string, end="\n"):
	print("\nAssistant:", string, end=end)
	global last_assistant
	last_assistant = string
	if not tts_off:
		thread = threading.Thread(target=say, args=(string,))
		thread.start()

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
					print_answer("Sorry, I don't know who " + search_item + " is.")
	else:
		answered = False
		try:
			search_item = search_item.replace("a ", "").strip()
			definition = dictionary.meaning(search_item)
			if definition:
				print_answer("Here are some definitions that I found: ")
				for part in definition:
					print("\t" + part + ":")
					for meaning in definition[part]:
						print("\t\t" + str(definition[part].index(meaning)+1) + ". " + meaning)
				answered = True
		except: pass
		if not answered:
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

def sleep(seconds):
	if seconds > 15: print_answer("A timer was set. Countdown has started.")
	elif seconds > 1: print_answer("A countdown has started.")
	print(seconds)
	time.sleep(seconds)
	print_answer("Time is over.")

def answer(user_input, user_input_without_syntax, words, question, greeting, about_themselves, statement, about_it, greeting_word):
	global tts_off, last_assistant, word_to_remove
	if user_input == "show me your knowledge":
		print_answer(str(data))

	elif user_input_without_syntax == "exit":
		with open("data.py", "w") as file:
			file.write(str(data))
		available_words = data["exit"].copy()
		available_words.remove("exit")
		available_words.remove("cya")
		available_words.remove("see you")
		print_answer(random.choice(available_words).capitalize())
		exit()

	elif user_input_without_syntax in data["exit"]:
		available_words = data["exit"].copy()
		available_words.remove("exit")
		available_words.remove("cya")
		available_words.remove("see you")
		print_answer(random.choice(available_words).capitalize())

	elif re.match(r"[\w\W]*shut[\w\W]*", user_input_without_syntax) and "mouth" in words or re.match(r"[\w\W]*tts-off[\w\W]*", user_input_without_syntax):
		tts_off = True

	elif re.match(r"[\w\W]*tts-on[\w\W]*", user_input_without_syntax):
		tts_off = False

	elif user_input_without_syntax == "what":
		print_answer(last_assistant)

	elif user_input_without_syntax == "say something":
		words = ["Hullo", "Sup", "Hulo", "Day", "Morning", "Evening", "Night", "Good morning!", "Good day!", "Good evening!", "Good night!", "Yo", "Afternoon", "Good afternoon!", "Halo", "Hallo", "Howdy"]
		available_words = data["greeting"].copy()
		for word in words: available_words.remove(word)
		print_answer(random.choice(available_words))

	if len(user_input) == 1:
		if user_input == ")":
			print_answer(")")
		elif user_input == "(":
			print_answer("(")

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

		if re.match(r"[\w\W]*and you", user_input_without_syntax) or re.match(r"[\w\W]*and what about you", user_input_without_syntax):
			user_input = last_assistant
			user_input_without_syntax = remove_syntax(last_assistant).lower().strip()
			question, greeting, about_themselves, statement, about_it, greeting_word = recognize_type(user_input, user_input_without_syntax, words)
			answer(last_assistant, user_input_without_syntax, user_input_without_syntax.split(), question, greeting, about_themselves, statement, about_it, greeting_word)
			for word in words:
				if word in data["good"]:
					word_to_remove = word
				if word in data["bad"]:
					word_to_remove = word
			return
	# if user said something about assistant
	if about_it:
		print("They said something about assistant")
		
		answered = False

		for noun in words:
			if not answered:
				for word in data["bad"]:
					if noun.startswith(word) or noun.endswith(word):
						print_answer("Please, contact @bekhruzniyazov on Tim's Discord and tell him the reason why you didn't like me. :(")
						answered = True
						break
			else:
				break
		if not answered:
			for noun in words:
				if not answered:
					for word in data["good"]:
						if noun.startswith(word) or noun.endswith(word):
							print_answer("Thanks a ton!")
							answered = True
							break
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

		elif greeting_word == "Good day!" or greeting_word == "Day" or greeting_word == "Good afternoon!" or greeting_word == "Afternoon":
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
				print_answer("Good afternoon!")
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

		if re.match(r"[\w\W]*glad[\w\W]*see[\w\W]*you", user_input_without_syntax):
			print_answer("Thanks")
			answered = True

		if not answered:
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
				words_to_remove = ["well", "outstanding", "terrific", "fine", "cool", "exceptional"]
				if word_to_remove not in words_to_remove and word_to_remove in available_words: available_words.remove(word_to_remove.strip())
				for wrd in words_to_remove:
					available_words.remove(wrd)
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
				words = ["Hullo", "Sup", "Hulo", "Day", "Morning", "Evening", "Night", "Good morning!", "Good day!", "Good evening!", "Good night!", "Yo", "Afternoon", "Good afternoon!", "Halo", "Hallo", "Howdy"]
				if greeting_word not in words: greetings.remove(greeting_word)
				for wrd in words:
					greetings.remove(wrd)

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

		if re.match(r"my [\w\W]+ is [\w\W]+", user_input_without_syntax):

			noun = re.findall(r"my [\w\W]+ is ([\w\W]+)", user_input_without_syntax)[0]

			for word in noun.split():

				if word in data["good"]:
					available_words = data["good"].copy()
					available_words.remove("well")
					available_words.remove("outstanding")
					available_words.remove("terrific")
					available_words.remove("fine")
					available_words.remove("cool")
					available_words.remove("exceptional")
					available_words.append("really well")
					print_answer(random.choice(available_words).capitalize())

				elif word in data["bad"]:
					print_answer(":(")

		if re.match(r"i am doing \w+ [\w\W]*", user_input_without_syntax):
			noun = re.findall(r"i am doing (\w+) [\w\W]*", user_input_without_syntax)[0]
			_not = False
			for word in data["good"]:
				if word == "not": _not = True
				if word in data["good"]:
					if _not:
						print_answer("Can I help you somehow?")
						break
					else:
						available_words = data["good"].copy()
						words_to_remove = ["terrific", "exceptional", "outstanding"]
						if word not in words: available_words.remove(word)
						for word in words_to_remove:
							available_words.remove(word)
						print_answer("That's " + random.choice(available_words) + "!")
						break

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

		if len(words) == 1:
			word = words[0]
			if word in data["good"]:
				print_answer("I feel really happy about that.")
			if word in data["bad"]:
				print_answer("What's wrong?")

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

		if re.match(r"set[ a]* timer$", user_input_without_syntax):
			seconds = 0
			while seconds <= 0:
				print_answer("How many seconds should I set timer for (enter a number)? ", end="")
				seconds = input()
				if seconds.isdigit(): seconds = int(seconds)
				else:
					print_answer("Timer canceled.")
					break

			if type(seconds) == int:
				if seconds > 0:							
					timer_thread = threading.Thread(target=sleep, args=(seconds,))
					timer_thread.start()
				else: print_answer("Timer was canceled.")
		
		elif re.match(r"set[ a]* timer for [\d]*[ hours\W]*[and ]*[\d]*[ minutes\W]*[and ]*[\d]*[ seconds\W]", user_input_without_syntax):
			hours, minutes, seconds = 0, 0, 0
			if "hours" in words or "hour" in words:
				try: hours = int(re.findall(r"\s([\d]+) hour", user_input_without_syntax)[0])
				except: pass
			if "minutes" in words or "minute" in words:
				try: minutes = int(re.findall(r"\s([\d]+) minute", user_input_without_syntax)[0])
				except: pass
			if "seconds" in words or "second" in words:
				try: seconds = int(re.findall(r"\s([\d]+) second", user_input_without_syntax)[0])
				except: pass
			
			time = seconds
			time += minutes * 60
			time += hours * 3600

			if time > 0:
				timer_thread = threading.Thread(target=sleep, args=(time,))
				timer_thread.start()
			else: print_answer("Timer was canceled.")

def main():
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

		question, greeting, about_themselves, statement, about_it, greeting_word = recognize_type(user_input, user_input_without_syntax, words)

		answer(user_input, user_input_without_syntax, words, question, greeting, about_themselves, statement, about_it, greeting_word)

def recognize_type(user_input, user_input_without_syntax, words):
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
			if user_input_without_syntax.startswith(remove_syntax(grtng).lower() + " "):
				greeting_word = grtng
				greeting = True
				break
			elif user_input_without_syntax.endswith(" " + remove_syntax(grtng).lower()):
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

				# last check
				if not question:
					if re.match("[\w\W]*and you", user_input_without_syntax) or re.match("[\w\W]*what[s]* about you", user_input_without_syntax):
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

	return question, greeting, about_themselves, statement, about_it, greeting_word

if __name__ == "__main__":
	main_thread = threading.Thread(target=main)
	main_thread.start()