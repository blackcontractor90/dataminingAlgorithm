import re
import enchant
from nltk.metrics import edit_distance
from nltk.corpus import wordnet

replacement_patterns = []

class RegexReplacer:
	#constructor that builds a list of tuples containing words and their contractions
	def _init_(self, patterns = replacement_patterns):
		self.patterns = [(re.compile(regex),repl) for (regex, repl) in patterns]
			
	#replaces words like can't, would've with full form
	
	def replace(self, text):
		s = text
		for (pattern, repl) in self.patterns:
			(s, count) = re.subn(pattern, repl, s)
		return s

class RepeatReplacer:
	def _init_(self):
		self.repeat_regex = re.compile(r'(\w*)(\w)\2(\w*)')
		self.repl = r'\1\2\3'
		
	def replace(self, word):
		if wordnet.synsets(word): 
			return word
		repl_word = self.repeat_regex.sub(self.repl, word)
		if repl_word != word:
			return self.replace(repl_word)
		else:
			return repl_word

class SpellingReplacer:
	
	def _init_(self, dict_name = 'en', max_dist = 2):
		
		self.spell_dict = enchant.Dict(dict_name)
		self.max_dist = max_dist
	
	def replace(self, word):
		if self.spell_dict.check(word):
			return word
			suggestions = self.spell_dict.suggest(word)
			if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
				return suggestions[0]
				else:
					return word
			
			