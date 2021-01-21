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

from subprocess import Popen

import smtplib

import webbrowser

import requests

import pyowm

# importing dataset from data.py file
from data import data

dictionary = PyDictionary()

last_assistant = ""

before_last_assistant = ""

tts_off = False

word_to_remove = ""

to_send_to_js = ""

printed = False

said = False

turnTTSOff = False

last_joke = ""

import eel

eel.init("web")

if len(argv) > 1:
	if argv[1] == "--tts-off":
		tts_off = True

def say(string):
	if len(string) < 150 and len(string) > 1:
		tts = gTTS(text=string)
		try:
			filename = "speech" + str(random.randint(0, 1000000)) + ".mp3"
			tts.save(filename)
			playsound(filename)
			os.remove(filename)
		except Exception as e: print(e)

@eel.expose
def send_to_js():
	global to_send_to_js, turnTTSOff, tts_off
	tmp = True if turnTTSOff else False
	turnTTSOff = False
	if tmp: tts_off = True
	to_send = to_send_to_js
	to_send_to_js = None
	if to_send:
		return to_send, tmp

@eel.expose
def print_answer(string, end="\n", tts=True):
	if string:
		print("\nAssistant:", string, end=end)
		global last_assistant, to_send_to_js, last_assistant2, to_send, printed, tts_off
		printed = True
		before_last_assistant = last_assistant
		last_assistant = string
		if not tts_off and tts:
			thread = threading.Thread(target=say, args=(string,))
			thread.start()
		to_send_to_js = string

@eel.expose
def remove_syntax(string):
	return re.sub("[,.!?\"']*", "", string)

@eel.expose
def toggle_tts():
	global tts_off
	tts_off = not tts_off

@eel.expose
def done():
	global to_send_to_js
	to_send_to_js = None

def get_input(string):
	global answer, to_send_to_js
	
	answer = string
	print_answer(answer)
	to_send_to_js = answer
	eel.get_input()
	
	value = eel.send_input_value()()
	while not value:
		value = eel.send_input_value()()
	return value

def send(string):
	global answer, send_to_js
	
	answer = string
	send_to_js = answer
	print_answer(answer)

def search(search_item, person):
	answer = ""
	if person:
		try:
			answer = search_wikipedia(search_item)
			found_on_wikipedia()
		except:
			try:
				answer = search_wikipedia(search_item.split()[-1])
				found_on_wikipedia()
			except:
				try:
					answer = search_wikipedia(search_item.split()[0])
					found_on_wikipedia()
				except:
					answer = "Sorry, I don't know who " + search_item + " is."
	else:
		answered = False
		try:
			search_item = search_item.replace("a ", "").strip()
			definition = dictionary.meaning(search_item)
			if definition:
				print_answer("Here are some definitions that I found: ")
				answer = ""
				for part in definition:
					answer += part + ":<br>"
					for meaning in definition[part]:
						answer += str(definition[part].index(meaning)+1) + ". " + meaning + ". <br>"
				answered = True
		except: pass
		if not answered:
			for category in data:
				if search_item in data[category]:
					answer = search_item + " is a " + category if search_item != category else search_item + " means " + random.choice(data[category])
					answered = True
		if not answered:
			answer = "Sorry, I don't know that yet. But you can teach me."
	return answer

def search_wikipedia(search_item):
	return wikipedia.summary(search_item)

def found_on_wikipedia():
	print_answer("Here is what I found on Wikipedia:")

def sleep(seconds):
	if seconds > 15: print_answer("A timer was set. Countdown has started.")
	elif seconds > 1: print_answer("A countdown has started")
	time.sleep(seconds)
	print_answer("Time is over")

@eel.expose
def generate_answer(user_input, user_input_without_syntax, words, question, greeting, about_themselves, statement, about_it, greeting_word):
	global tts_off, last_assistant, word_to_remove, printed, to_send_to_js, said, turnTTSOff, last_joke

	user_input = user_input.lower()

	answer = ""

	printed = False

	if user_input == "show me your knowledge":
		answer = str(data)
		print_answer(answer)

	elif "weather" in words:
		temperature = pyowm.OWM("6d00d1d4e704068d70191bad2673e0cc").weather_manager().weather_at_place(eel.get_location()()).weather.temperature("celsius")["temp"]
		answer = "Right now, in " + eel.get_location()() + " it is " + str(temperature) + "°C"
		print_answer(answer)

	elif "joke" in words and "not" not in words:
		jokes = data["jokes"].copy()
		if last_joke in jokes: jokes.remove(last_joke)
		answer = random.choice(jokes)
		last_joke = answer
		print_answer(answer)

	elif "time" in words:
		answer = "Right now it is " + str(datetime.now().time())[:8]
		print_answer(answer)

	elif "date" in words:
		answer = "Right now it is " + str(datetime.now().date())
		print_answer(answer)

	elif user_input_without_syntax == "exit":
		with open("data.py", "w") as file:
			file.write("data = " + str(data))
		available_words = data["exit"].copy()
		available_words.remove("exit")
		available_words.remove("cya")
		available_words.remove("see you")
		available_words.remove("see ya")
		answer = random.choice(available_words).capitalize()
		print_answer(answer)
		exit()

	elif user_input_without_syntax in data["exit"]:
		available_words = data["exit"].copy()
		available_words.remove("exit")
		available_words.remove("cya")
		available_words.remove("see you")
		answer = random.choice(available_words).capitalize()
		print_answer(answer)

	elif re.match(r"[\w\W]*shut[\w\W]*", user_input_without_syntax) and "mouth" in words or re.match(r"[\w\W]*shut up[\w\W]*", user_input_without_syntax) or user_input_without_syntax == "silence" or user_input_without_syntax == "quiet" or re.match(r"[\w\W]*be quiet[\w\W]*", user_input_without_syntax):
		tts_off = True
		answer = "Okay"
		turnTTSOff = True
		print_answer(answer)

	elif user_input_without_syntax == "what" or "say again" in user_input_without_syntax:
		answer = last_assistant
		print_answer(answer)

	elif re.match(r"[\w\s]*say [\w\s]*something[\w\s]*", user_input_without_syntax):
		words = ["Hullo", "Sup", "Hulo", "Day", "Morning", "Evening", "Night", "Good morning!", "Good day!", "Good evening!", "Good night!", "Yo", "Afternoon", "Good afternoon!", "Halo", "Hallo", "Howdy"]
		available_words = data["greeting"].copy()
		for word in words: available_words.remove(word)
		answer = random.choice(available_words)
		print_answer(answer)

	if len(user_input) == 1:
		if user_input == ")":
			answer = ")"
			print_answer(answer)
		elif user_input == "(":
			answer = "("
			print_answer(answer)

	# if user's input is a question
	if question:
		print("This is a question")
		if re.match(r"what does [\w\s]+ mean", user_input_without_syntax):

			search_item = user_input_without_syntax[user_input_without_syntax.index("does") + len("does") + 1 : user_input_without_syntax.index("mean")].strip()

			answer = search(search_item, False)
			print_answer(answer, tts=False)
		else:
			if re.match(r"wh[\w]*[is\s]*[\w\s]+", user_input_without_syntax):
				search_item = re.findall(r"wh[\w]*[is\s]*([\w\s]+)", user_input_without_syntax)[0]
				answer = search(search_item, False if words[0] == "what" else True)
				print_answer(answer, tts=False)

		if re.match(r"[\w\W]*and you[\w\W]*", user_input_without_syntax) or re.match(r"[\w\W]*what about you[\w\W]*", user_input_without_syntax):
			user_input = before_last_assistant
			user_input_without_syntax = remove_syntax(before_last_assistant).lower().strip()
			words = user_input_without_syntax.split()
			question, greeting, about_themselves, statement, about_it, greeting_word = recognize_type(user_input, user_input_without_syntax, words)
			if not question:
				user_input = last_assistant
				user_input_without_syntax = remove_syntax(last_assistant).lower().strip()
				words = user_input_without_syntax.split()
				question, greeting, about_themselves, statement, about_it, greeting_word = recognize_type(user_input, user_input_without_syntax, words)
			answer = generate_answer(user_input, user_input_without_syntax, words, question, greeting, about_themselves, statement, about_it, greeting_word)
			print_answer(answer)
			return answer
	# if user said something about assistant
	if about_it:
		print("They said something about assistant")
		
		answered = False

		for noun in words:
			if not answered:
				for word in data["bad"]:
					if noun.startswith(word) or noun.endswith(word):
						answer = "Please, contact @bekhruzniyazov on Tim's Discord and tell him the reason why you didn't like me. :("
						print_answer(answer)
						answered = True
						break
			else:
				break
		if not answered:
			for noun in words:
				if not answered:
					for word in data["good"]:
						if noun.startswith(word) or noun.endswith(word):
							answer = "Thanks a ton!"
							print_answer(answer)
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
					answer = "It is no longer morning, I believe. It is already afternoon."
					print_answer(answer)
					answered = True
				elif hour < 20:
					answer = "It is evening now. Good evening to you!"
					print_answer(answer)
					answered = True
				else:
					answer = "Good night. It's night now."
					print_answer(answer)
					answered = True
			else:
				answer = "Good morning!"
				print_answer(answer)
				answered = True

		elif greeting_word == "Good day!" or greeting_word == "Day" or greeting_word == "Good afternoon!" or greeting_word == "Afternoon":
			if hour < 12 or hour > 17:
				if hour < 12:
					answer = "It is only morning yet, I believe. Good morning to you!"
					print_answer(answer)
					answered = True
				elif hour > 17:
					answer = "It is evening now."
					print_answer(answer)
					answered = True
				elif hour > 20:
					answer = "Good night. It is night now."
					print_answer(answer)
					answered = True
			else:
				answer = "Good afternoon!"
				print_answer(answer)
				answered = True

		elif greeting_word == "Good evening" or greeting_word == "Evening":
			if hour < 17 or hour > 20:
				if hour < 12:
					answer = "It is only morning now. Good morning!"
					print_answer(answer)
				elif hour < 17:
					answer = "It is not evening yet. Good day to you!"
					print_answer(answer)
					answered = True
				elif hour > 20:
					answer = "It is night now. Good night to you!"
					print_answer(answer)
					answered = True
			else:
				answer = "Good evening!"
				print_answer(answer)
				answered = True

		elif greeting_word == "Good night!" or greeting_word == "Night":
			if hour < 20 or hour > 6:
				if hour < 20:
					answer = "It is not night yet."
					print_answer(answer)
					answered = True
				elif hour > 6:
					answer = "It is no longer night."
					print_answer(answer)
					answered = True
			else:
				answer = "Good night to you!"
				print_answer(answer)
				answered = True

		if re.match(r"[\w\W]*glad[\w\W]*see[\w\W]*you", user_input_without_syntax):
			answer = "Thanks"
			print_answer(answer)
			answered = True

		if not answered:
			# answering to the user

			# if user asked "what's up?"
			if greeting_word == "What's up?" or greeting_word == "Sup":
				responses = ["Nothing", "Not much", "All right"]
				answer = random.choice(responses)
				print_answer(answer)

			# if user did not ask "what's up?" but they asked "how are you" or "how do you do" or "how are you doing"
			elif greeting_word == "How are you?" or greeting_word == "How do you do?" or greeting_word == "How are you doing?":

				# creating an answer variable; at start one word will be appended to it
				answer = random.choice(["Everything is ", "I feel "])

				# creating a copy of data["good"] list
				available_words = data["good"].copy()

				# filtering the list from unwanted words
				words_to_remove = ["well", "outstanding", "terrific", "fine", "cool", "exceptional"]
				if word_to_remove not in words_to_remove and word_to_remove in available_words: available_words.remove(word_to_remove.strip())
				for wrd in words_to_remove:
					available_words.remove(wrd)
				available_words.append("really well")

				# appending a word to the answer
				answer += random.choice(available_words)

				# answering to the user
				print_answer(answer)

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
				answer = random.choice(greetings)
				print_answer(answer)

	# if user's input is a statement about themselves
	if about_themselves:

		print("This is a statement about themselves")
		
		if re.match(r"i [do ]*feel [\w\s]+[,]*[\w\s]*", user_input_without_syntax, re.IGNORECASE):

			their_feelings = re.findall(r"i [do ]*feel ([\w\s]+)?,*[\w\s]*", user_input_without_syntax, re.IGNORECASE)[0]

			answered = False

			for word in their_feelings.split():

				word = word.strip()
				
				if word in data["good"]:
					print_answer("Glad you do")
					answered = True
					break
				
				elif word in data["bad"]:
					answer = "Can I cheer you up somehow? You can ask me for a joke."
					print_answer(answer)
					answered = True
					break

			if not answered:
				answer = "Sorry, but I don't know what \"" + their_feelings + "\" means."
				print_answer(answer)

		if re.match(r"i am a[n]* [\w\s]+", user_input_without_syntax):

			answered = False

			noun = re.findall(r"i am a[n]* ([\w\s]+)", user_input_without_syntax)[0]

			for word in noun.split():

				word = word.strip()

				if word in data["good"]:
					answer = "I agree with you."
					print_answer(answer)
					answered = True
					break

				elif word in data["bad"]:
					answer = "I feel so sorry about that. Can I help you somehow?"
					print_answer(answer)
					answered = True
					break

			if not answered:
				answer = "I am sorry, but I do not know what \"" + noun + "\" means."
				print_answer(answer)

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
					answer = random.choice(available_words).capitalize()
					print_answer(answer)

				elif word in data["bad"]:
					answer = ":("
					print_answer(answer)

		if re.match(r"i am doing \w+ [\w\W]*", user_input_without_syntax):
			noun = re.findall(r"i am doing (\w+) [\w\W]*", user_input_without_syntax)[0]
			_not = False
			for word in data["good"]:
				if word == "not": _not = True
				if word in data["good"]:
					if _not:
						answer = "Can I help you somehow?"
						print_answer(answer)
						break
					else:
						available_words = data["good"].copy()
						words_to_remove = ["terrific", "exceptional", "outstanding"]
						if word not in words: available_words.remove(word)
						for word in words_to_remove:
							available_words.remove(word)
						answer = "That's " + random.choice(available_words) + "!"
						print_answer(answer)
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
				answer = "I feel really happy about that." if not said and "feel" not in last_assistant else ")"
				print_answer(answer)
				said = not said
			if word in data["bad"]:
				answer = "What's wrong?"
				print_answer(answer)

		if user_input_without_syntax == "same" or re.match("i feel[ the]* same[\w ]*", user_input_without_syntax):
			user_input = last_assistant
			user_input_without_syntax = remove_syntax(last_assistant).lower().strip()
			words = user_input_without_syntax.split()
			question, greeting, about_themselves, statement, about_it, greeting_word = recognize_type(user_input, user_input_without_syntax, words)
			answer = generate_answer(user_input, user_input_without_syntax, words, question, greeting, about_themselves, statement, about_it, greeting_word)
			print_answer(answer)
			return answer

		if re.match(r"open [\w|\s]+", user_input.lower().strip()):
			application = re.findall(r"open ([\w\W]+)", user_input.lower().strip())[0].strip()
			request = requests.get("http://" + application if not application.startswith("http") else application)
			if request.status_code == 200:
				webbrowser.open(application)
			else:
				try:
					os.system(application)
				except:
					try:
						Popen(application)
					except: pass

		if re.match(r"send[(a)|(an)\s]*[(email)|(message)\s]+[(please)|(cant you)\s]", user_input_without_syntax):
			try:
				email = data["email"]
				password = data["password"]
			except:
				email = get_input("Please, type in your email address")
				if email.lower() == "cancel": return
				password = get_input("Please, type in your password")
				if password.lower() == "cancel": return
				remember = get_input("Do you want me to remember them? (y|n)")
				if remember.lower() == "cancel": return
				if remember == "y":
					data["email"] = email
					data["password"] = password
					with open("data.py", "w") as file:
						file.write("data = " + str(data))
			to_email = get_input("Please, type the email address of a person you want to send this email to")
			if to_email.lower() == "cancel": return
			subject = get_input("Please, enter the subject of the email")
			if subject.lower() == "cancel": return
			body = get_input("Please, enter the body of the email")
			if body.lower() == "cancel": return

			try:
				server = smtplib.SMTP("smtp." + email[email.index("@")+1:], 587)
				server.starttls()
				server.login(email, password)
				message = "Subject: " + subject + "\n\n" + body
				server.sendmail(email, to_email, message)
				send("Email was sent")
			except Exception as e:
				print(e)
				data.pop("email", "")
				data.pop("password", "")
				with open("data.py", "w") as file:
					file.write("data = " + str(data))
				answer = "Sorry, an error occurred"
				to_send_to_js = answer
				print_answer(answer)

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
			seconds = get_input("How many seconds should I set timer for?")
			if seconds.isdigit(): seconds = int(seconds)
			else:
				answer = "Timer canceled."
				to_send_to_js = answer
				print_answer(answer)

			if type(seconds) == int:
				if seconds > 0:							
					timer_thread = threading.Thread(target=sleep, args=(seconds,))
					timer_thread.start()
				else:
					answer = "Timer was canceled."
					print_answer(answer)
		
		elif re.match(r"set[ \w]* timer for [\d]*[ hours\W]*[and ]*[\d]*[ minutes\W]*[and ]*[\d]*[ seconds\W]", user_input_without_syntax):
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
			else:
				answer = "Timer was canceled."
				print_answer(answer)

		elif re.match(r"[\w\W]*thank you[\w\W]*", user_input_without_syntax) or user_input_without_syntax == "thanks" or user_input_without_syntax.endswith("thanks") or user_input_without_syntax.replace(" a ", " ").endswith("thanks ton") or user_input_without_syntax.startswith("thanks for"):
			answer = "You are welcome"
			print_answer(answer)

		elif re.match(r"[\w\W]*nice[\w\W]to[\w\W]*you[\w\W]*", user_input_without_syntax):
			answer = "Thanks"
			print_answer(answer)

	if not printed:
		to_send_to_js = ""

@eel.expose
def recognize_type(user_input, user_input_without_syntax, words):
	question = False
	greeting = False
	about_themselves = False
	statement = False
	about_it = False

	user_input = user_input.lower()

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
		
		if len(user_input) > 2:
			for word in data["self"]:
				if word in words:
					if word == "youre" or word == "you" and "are" in words or word == "you're":
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
						word = word.lower()
						if word in data["themselves"]:
							if word == "my":
								if "is" in words: statement = True
							about_themselves = True
							break

					# if user's input is not a greeting or a question or a statement about themselves/their feelings
					if not about_themselves:
						statement = True

					# TODO: add "remember this" (should be a list)
					# TODO: add built-in calculator
					# TODO: add "what can you do"
					# TODO: add "who are you"
					# TODO: add all reminders in a list
					# TODO: add translator
					# TODO: add random number generator
					# TODO: try to add some sort of built-in google search
					# TODO: try to add a control over volume and brightness
					# TODO: if I have enough time: add image and file sharing tool
					# TODO: add wake word

	return question, greeting, about_themselves, statement, about_it, greeting_word

if __name__ == "__main__":
	eel.start("index.html", size=(550, 900))