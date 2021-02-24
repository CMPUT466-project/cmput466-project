# Author: Shway Wang，Shiyu Xiu
import string
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
DATA_PATH = './datasets/' # the place to read from
PROCESSED_PATH_WITHSTOPWORD='./processed_datasets/'
PROCESSED_PATH = './processed_datasets2/' # the place to write to and delete stopwords

'''
The categories are:
business(510), entertainment(386), politics(417), sport(511), tech(401)
'''
subpaths = {'business': 510, 'entertainment': 386, 'politics': 417, 'sport': 511, 'tech': 401}
def preprocess_all():

	for folder in subpaths:
		for i in range(1, subpaths[folder] + 1):
			temp_lines = []
			if (i < 10): i = '00%d' % i
			elif (i < 100): i = '0%d' % i
			else: i = str(i)
			
			# News_Articles:
			try:
				with open(DATA_PATH + 'News_Articles/%s/%s.txt' % (folder, i), 'r',encoding="utf8") as f:
					# ignore the title
					temp_lines = f.readlines()[1:]
					content = ''
					for sentence in temp_lines:
						temp = sentence.rstrip()
						if temp[-1:] == '.': temp += ' '
						content += temp
					# want to make a line for each sentence
					temp_lines = content.split('. ')
					for j in range(len(temp_lines)):
						# remove all punctuations and make lowercase
						temp_lines[j] = temp_lines[j].translate(str.maketrans('', '', string.punctuation)).lower()
				# write the result to the corresponding folders:
				with open(PROCESSED_PATH + 'proced_News_Articles/%s/%s.txt' % (folder, i), 'w',encoding="utf8") as f:
					for sentence in temp_lines:
					#for removing some common stopwords like "is","a","for" et
						text_tokens = word_tokenize(sentence)
						list_wt_sw = [word for word in text_tokens if not word in stopwords.words()]
						sentence=(" ").join(list_wt_sw)
						f.write(sentence+"\n")
			except:
				print("Encoding error encountered when reading file: %s %s" % (folder, i))
			

			# Summaries:
			with open(DATA_PATH + 'Summaries/%s/%s.txt' % (folder, i), 'r',encoding="utf8") as f:
				content = ''
				for sentence in temp_lines:
					temp = sentence.rstrip()
					if temp[-1:] == '.': temp += ' '
					content += temp
				# want to make a line for each sentence
				temp_lines = f.read().split('. ')
				for j in range(len(temp_lines)):
					# remove all punctuations and make lowercase
					temp_lines[j] = temp_lines[j].translate(str.maketrans('', '', string.punctuation)).lower()
			# write the result to the corresponding folders:
			with open(PROCESSED_PATH + 'proced_Summaries/%s/%s.txt' % (folder, i), 'w',encoding="utf8") as f:
				for sentence in temp_lines:
					#for removing some common stopwords like "is","a","for" etc
					text_tokens = word_tokenize(sentence)
					list_wt_sw = [word for word in text_tokens if not word in stopwords.words()]
					sentence=(" ").join(list_wt_sw)
					f.write(sentence + "\n")


if __name__ == '__main__':
	preprocess_all()