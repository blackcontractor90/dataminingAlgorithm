import re
from FileOps imprt readAbbrFile, readStopwordsFile
from nltk.stem import WordNetLemmatizer an wnl
from nltk.tokenize import word_tokenize
import string


exclude = set(string.punctuation)
stopWordsFile = '' #stopwords list
abbrFile = '' #abbreviation text list

#isolates texts into positive, negative, neutral, and mixed texts
def clean_data(original_tweets):
	pos_tweets = []
	neg_tweets = []
	neu_tweets = []
	mix_tweets = []
	
	for tweet, sentiment in original_tweets:
		if_sentiment == 0.0:
			neu_tweets.append((process_tweet(tweet), sentiment))
			elif sentiment == 2.0:
				mix_tweets.append((process_tweet(tweet), sentiment))
				elif sentiment == 1.0:
					pos_tweets.append((process_tweet(tweet), sentiment))
					elif sentiment == -1.0:
						neg_tweets.append((process_tweet(tweet), sentiment))
						return pos_tweets, neg_tweets, neu_tweets, mix_tweets
	
	#function to clean data (no need for this case!)
	def process_tweet(tweet):
		#remove urls
		tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','',tweet)
		
		#replace 2 or more repetitions of a character
		tweet = replaceTwoOrMore(tweet)
		
		#remove username
		tweet = re.su('@[^\s]+','',tweet)
		
		#replace /word with word
		tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
		
		#replace hex code with single quote
		tweet = re.sub(r'\\xe2\\x80\\x99', "'", tweet)
		
		#removing <e> and <a> tags
		tweet = re.sub(r'(<e>|</e>|<a>|</a>|\n)', '', tweet)
		
		#remove punctuation
		tweet = ''.join(ch for ch in tweet if ch not in exclude)
		
		#remove words that end with digits
		tweet = re.sub(r'\d+','',tweet)
		
		#removing words that start with a number or a special character
		tweet = re.sub(r"^[^a-zA-Z]+", ' ', tweet)
		
		#remove additional white spaces
		tweet = re.sub('[\s]+', ' ', tweet)
		
		#replace all words that dont start with a letter, number or underscore with an empty string
		tweet = re.sub(r'\\[xa-z0-9.*]+', '', tweet)
		
		#remove trailing spaces and full stops
		tweet = tweet.strip(' .')
		
		#convert camel case words to space delimited words
		tweet = convertCamelCase(tweet)
		
		#convert everything to lower characters
		tweet = tweet.lower()
		
		#tokenize the text
		tweet = tokenize_tweet(tweet)
		
		#replace abbreviations with their corresponding meanings
		tweet = replaceAbbr(tweet)
		
		#lemmatize the words in tweets
		tweet = wordLemmatizer(tweet)
		
		#remove stopwords from the tweet
		tweet = removeStopWords(tweet, stopwords)
		
		#removing duplicates
		tweet = list(set(tweet))
		
		return tweet
		
	#------end------
	
	#remove stopwords
	def removeStopWords(tweet, stopwords):
		tmp = []
		for i in tweet:
			if i not in stopwords:
				tmp.append(i)
				
		return tmp
		
	
	def replaceTwooOrMore(s):
	#look for 2 or more repetitions of character
		pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
		return pattern.sub(r"\1\1", s)
	
	def convertCamelCase(word):
		return re.sub("([a-z])([A-Z])","\g<1> \g<2>",word)
		
	def is_ascii(self, word):
		return all(ord(c) < 128 for c in word)
	
	def replaceAbbr(s):
		for word in s:
			if word.lower() in abbr_dict.keys():
			s = [abbr_dict[word.lower()] if word.lower() in abbr_dict.keys() else word for word in s]
		return s
	
	def tokenize_tweet(tweet):
		return word_tokenize(tweet)
	
	def wordLemmatizer(tweet_words):
		return [wnl().lemmatize(word) for word in tweet_words]
