# These are the emails you will be censoring. The open() function is opening the text file that the emails are contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithm", "her", "herself", "Helena"]
negative_words = ["concerned", "behind", "danger", "dangerous", "alarmingly", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed", "distressing", "concerning", "horrible", "horribly", "questionable"]
punctuation = [".", ",", "?", "!"]
#This function generates and returns redacted text
def redact(word):
	return "X"*len(word)

#This function counts how many negative words are in a text
def count_neg_words(negative_words, text):

	neg_words = []		#List of single words like "bad", "sad", "mad"
	neg_phrases = []	#List of words that have spaces like "sense of self" or "out of control"
	count = 0

	#Seperate the neg_phrases from the negative words
	for word in negative_words:
		if word.count(" ") > 0:
			neg_phrases.append(word)
		else:
			neg_words.append(word)

	paragraphs = text.split('\n')

	for paragraph in paragraphs: 	

		for phrase in neg_phrases:		#It's easier to look for phrases in a big block text
			count += paragraph.count(phrase)

		words = paragraph.split()		#Breaking down the paragraph into words, so that it will be easier to compare words to words
		
		for word in words:
			for neg_word in neg_words:		#Comparing each neg_word to a word in paagraph
				if neg_word in word or neg_word.upper() in word or neg_word.title() in word: #Ex: neg_word = "help", "HELP", or "Help"
					count += 1	

	return count

#Given a phrase and string of text, this function returns the text that has the censored phrase redacted.
def censor_phrase(phrase, text):
	redacted = redact(phrase)
	return text.replace(phrase, redacted)

#Given a keyword and a string of text, this function return the text that has that word censored regardless
#if it has a punction attached to the end of it or has a captial letter at the beginning.
def censor_word(keyword, text):

	paragraphs = text.split('\n')
	new_paragraphs = []
	new_paragraph = ""

	for paragraph in paragraphs:
		new_words = []
		words = paragraph.split()
		for word in words:
			if keyword.title() in word or keyword.upper() in word or keyword in word:
				if len(word) == len(keyword):
					redacted = redact(keyword)
					word = redacted
					new_words.append(word)
				elif len(word) == len(keyword) + 1:
					if word[-1] in punctuation:
						sp_char = word[-1]
						word = word.strip(word[-1])
						redacted = redact(keyword)+sp_char
						word = redacted
						new_words.append(word)
						sp_char = ""
					else:
						new_words.append(word)
				else:
					new_words.append(word)
			else:
				new_words.append(word)

		new_paragraph = ' '.join(new_words)
		new_paragraphs.append(new_paragraph)

	return '\n'.join(new_paragraphs)

#This function take in a list of words and return the censored text.
def censor_two(censor_words, text):
	words = []
	phrases = []

	for word in censor_words:		#Need to see if it is a word or phrase
		if word.count(" ") > 0: 		#If the word contains spaces it is a phrase
			phrases.append(word)
		else:							#If the word doesn't, then it is a word
			words.append(word)

	for phrase in phrases:
		text = censor_phrase(phrase, text)

	print(text, "A")
	for word in words:
		text = censor_word(word, text)
	print(text, "B")

	return text

email_two_redacted = censor_two(proprietary_terms, email_two)
print(email_two_redacted, '\n-------------\n')

#This function takes in two lists of words, censored_words and neg_words and returns the censored text
def censor_three(censored_words, neg_words, text):
	text = censor_two(censored_words, text)

	neg_count = count_neg_words(neg_words, text)

	if neg_count > 2:								#Gotta see if more than two negative words are in, if so we censor all of them
		text = censor_two(negative_words, text)

	return text

#print(count_neg_words(negative_words, email_three))

email_four_redacted = censor_three(proprietary_terms, negative_words, email_four)
#print(email_four_redacted)