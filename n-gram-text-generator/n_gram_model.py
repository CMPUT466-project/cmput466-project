'''
Created on 7 nov. 2015

@author: Antonin Duroy
'''

import codecs
import numpy as np

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import ConditionalFreqDist
from nltk.util import ngrams
from scipy import stats

from utils import get_none_tuple, get_none_list
from realizer import Realizer

class NgramModel:
    
    def __init__(self, filepath, lang='english'):
        self.text = self._load_file(filepath)
        self.lang = lang
        self.sentences = sent_tokenize(self.text, language=self.lang)
        self.seted_sent = None

    
    def _load_file(self, filepath):
        with codecs.open(filepath, 'r', encoding='utf-8') as f:
            return f.read().replace('\n', ' ').lower()
    
    def _select_nextword(self, ngram, cfdist=None):
        """ Select a word from a range of possibilities, given a frame of
        (n-1) words previously generated.
        """
        xk = np.arange(cfdist[ngram].B())
        #print(cfdist[ngram].B())
        #print(ngram)
        pk = []
        candidates = []
        for next_word in cfdist[ngram]:
            candidates.append(next_word)
            pk.append(cfdist[ngram].freq(next_word))
        print(pk)
        print(candidates)
        custm = stats.rv_discrete(values=(xk, pk))
        #print(custm.rvs())
        return candidates[custm.rvs()]

    def set_sent(self, sent):
        self.seted_sent = word_tokenize(sent.lower(), language=self.lang)

    def gen_text(self, n, nb_sents=None, nb_words=None):
        """ Enable text generation.
        """
        if n < 1:
            raise ValueError("n must be higher or equal than 1.")
        if nb_sents is None and nb_words is None:
            raise ValueError("nb_sents or nb_words must be set.")
        
        tok_sents = [get_none_list(n-1)+word_tokenize(sentence, language=self.lang) for sentence in self.sentences]
        words = []
        for tok_sent in tok_sents:
            words += tok_sent
        words += [None] # None is set as the end of a sentence
        
        # Compute conditional frequency distribution for each n-gram
        ngrams_ = ngrams(words, n)
        ngrams_cfd = ConditionalFreqDist((ngram[:-1], ngram[-1]) for ngram in ngrams_)
        frame = get_none_tuple(n-1)
        gen_tokens = []
        nb_sents_gen = 0
        nb_word_gen = 0
        for i in self.seted_sent:
            frame += (i,)
            frame = frame[1:]
            gen_tokens.append(i)
        while True:
            if nb_words is not None and nb_word_gen == nb_words:
                break
            new_word = self._select_nextword(frame, ngrams_cfd)
            if new_word is None:
                nb_sents_gen += 1
                if nb_sents is not None and nb_sents_gen == nb_sents:
                    break
                frame = get_none_tuple(n-1)
                continue
            frame += (new_word,)
            frame = frame[1:]
            gen_tokens.append(new_word)
            nb_word_gen += 1
        
        realizer = Realizer(lang=self.lang)
        return realizer.realize(gen_tokens)

if __name__ == '__main__':
    ngramModel = NgramModel('../data/business.txt', lang='english')
    ngramModel.set_sent("I am")
    text = ngramModel.gen_text(5, nb_words=8)
    print(text)