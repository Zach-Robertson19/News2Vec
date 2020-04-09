import pandas as pd 
import numpy as np
from collections import Counter
from itertools import chain
import pickle
import operator
import gensim 
from gensim.models import Word2Vec 
from nltk.tokenize import sent_tokenize, word_tokenize 
import warnings 
import sys 
import math
import os
from langdetect import detect
from langdetect import DetectorFactory
import re
from urllib.parse import urlparse
import difflib
from spellchecker import SpellChecker

# Creates a Word2Vec Model and saves it as a bin file
class Word2Vec_Model:
    '''
    Object that creates a Word2Vec Model and saves it as a bin file. Uses the data
    created in the subreddit_data_to_csv.py file and parses it for punctuation for
    easier manipulation. The parsed sentences are saved as a pickle file for
    retrevial later.

    Parameters:
        csv_file (str) : csv file created by the subreddit_data_to_csv.py file
    '''
    def __init__(self, csv_file):
        self.csv_filename = csv_file
        self.model_name = csv_file[:-4] + '_W2VModel'
        if os.path.isfile(self.model_name + '.bin'):
            print('Model already exis for this time range')
        else:
            print('Model doesn\'t exist, creating model')
            if os.path.isfile(self.csv_filename[:-4] + '_sent.pkl'):
                print('Pickle file found')
                self.df = pd.read_pickle(csv_file[:-4] + '_sent.pkl')
                self.words = self.df['sent'].to_list()
            else:
                self.data = pd.read_csv(csv_file, header=0)
                self.df = self.word_array(self.data)
                self.words = self.df['sent'].to_list() 
            self.create_model(self.words, self.model_name)

    def create_model(self, words, model_name):
        data = []
        s = ' '
        for item in words:
            sent = s.join(item)
            for i in sent_tokenize(sent):
                temp = []
                for j in word_tokenize(i):
                    temp.append(j.lower())
                data.append(temp)

        model = Word2Vec(words, min_count=1, size=100, window=5, sg=1)  
        model.wv.save_word2vec_format(f'{model_name}.bin', binary=True)
        return model

    def word_array(self, data, pkl=True):
        DetectorFactory.seed = 0 

        
        sentences = pd.DataFrame(columns=['title', 'sent', 'url'])
        words = 0

        for i, (title, url) in enumerate(zip(data['title'], data['url'])):
            try:
                if detect(title) != 'en':
                    del df[i]
            except:
                pass
            word_line = []
            word_line_punct = list(re.split(r'\s+', title))

            for word in word_line_punct:
                word_punct = list(filter(None, re.split(r'(^(?:[A-Z]*[a-z]+\'[st])|^(?:[A-Z]*[a-z]+[s]\')|^(?:[A-Z]\.){1,2}|[^a-zA-Z])', word)))
                for elem in word_punct:
                    punct_match = re.match(r'[^a-zA-Z0-9]', elem)
                    if punct_match != None:
                        pass
                    else:
                        word_line.append(elem.lower())
                        words += 1
            url = urlparse(url).hostname
            sentences.at[i, 'title'] = title
            sentences.at[i, 'sent'] = word_line
            sentences.at[i, 'url'] = url
            

        pick_filename = str(self.csv_filename)[:-4] + '_sent.pkl'
        #pickle the word list
        if pickle:
            sentences.to_pickle(pick_filename, protocol=4)
            print(f'Pickle file added {pick_filename}')
        return sentences

# reads a Word2Vec Model and compares sentences using it
class Compare_Headlines:
    '''
    Object that finds the cosine similarity between the subreddit titles given in
    the title variable, calculated with the use of the model defined in model_name.
    These are the models created by the Word2Vec_Model Object.

    Parameters:
        model_name (str) : name of the model you want to use to find the cosine similarity.
            The titles should not be included in the model
        
        titles (list of strings) : The title strings that you want to find the cosine
            similarity of. If there are more than 2 titles you will get the cosine
            similarity of all of the groupings.
    '''
    def __init__(self, model_name, titles):
        self.model = self.read_model(model_name)
        self.pickle_file = model_name[:-9] + '_sent.pkl'
        self.vectors, self.titles = self.TDIDF_Sentence_Vectors(model_name, titles)

    def read_model(self, model_name):
        model = gensim.models.KeyedVectors.load_word2vec_format(model_name + '.bin', binary=True)
        return model

    def TDIDF_count(self, sent_words):
        rawcount_dict = dict(Counter(chain.from_iterable(sent_words)))
        TF_dict = dict(Counter(chain.from_iterable(set(i) for i in sent_words)))
        
        dict_list = list()
        
        for sent in sent_words:
            count_list = list()
            for elem in sent:
                count = rawcount_dict[elem]/len(sent)
                count_list.append(count)
            sent_dict = dict(zip(sent, count_list))
            dict_list.append(sent_dict)
        return dict_list, TF_dict

    def TDIDF_Sentence_Vectors(self, model_name, titles):
        model = self.read_model(model_name)
        sent_words = pd.read_pickle(self.pickle_file)
        _, TF_dict = self.TDIDF_count(sent_words['sent'].to_list())
        sent_vectors =[]
        sentences = []
        titles = Eleminate_Punctuation().eleminate_punctuation(titles)['sent'].to_list()
        
        
        for item in titles:
            weights = []
            w2v_vectors = []
            weighted_vectors = []
            for j, i in enumerate(item):
                
                try:
                    word_vector = model[i]
                    weight = TF_dict[i]
                except:
                    word = list(set(difflib.get_close_matches(i, [item for sublist in sent_words['sent'].to_list() for item in sublist])))
                    for element in word:
                        word = SpellChecker().correction(element)
                    word_vector = model[word]
                    weight = TF_dict[word]
                    item[j] = word
                weights.append(weight)
                w2v_vectors.append(word_vector)

            for index, j in enumerate(w2v_vectors):
                TD_vector = weights[index]*j
                weighted_vectors.append(TD_vector)

            sent_vector = np.zeros(shape=TD_vector.shape)
            for word_vector in weighted_vectors:
                sent_vector = np.add(sent_vector, word_vector)
            sent_vectors.append(sent_vector)
            sentences.append(' '.join(item))
        sent_vector_dict = dict(zip(sentences, sent_vectors))
        titles = [' '.join(item) for item in titles]
        return sent_vector_dict, titles

    def CosineSimilarity(self, sent_vector_dict, sent1, sent2):
        vector1 = sent_vector_dict[sent1]
        vector2 = sent_vector_dict[sent2]
        dot_product = np.dot(vector1, vector2)
        mag1 = np.linalg.norm(vector1)
        mag2 = np.linalg.norm(vector2)

        cos_sim = dot_product / (mag1*mag2)
        return cos_sim

# object used to manipulate sentences to eleminate punctuation
class Eleminate_Punctuation:
    '''
    Object that takes a list of string sentences and returns a list
    of lists that contain the words in the sentences without punctuation.

    Parameters:
        string_list (list of sentence strings) : list of sentence strings to have
            their punctuation eleminated. 
    '''
    def eleminate_punctuation(self, string_list):
        DetectorFactory.seed = 0
        sentences = pd.DataFrame(columns=['sent'])
        for i, item in enumerate(string_list):
            word_line = []
            word_line_punct = list(re.split(r'\s+', item))

            for word in word_line_punct:
                word_punct = list(filter(None, re.split(r'(^(?:[A-Z]*[a-z]+\'[st])|^(?:[A-Z]*[a-z]+[s]\')|^(?:[A-Z]\.){1,2}|[^a-zA-Z])', word)))
                for elem in word_punct:
                    punct_match = re.match(r'[^a-zA-Z0-9]', elem)
                    if punct_match != None:
                        pass
                    else:
                        word_line.append(elem.lower())
            sentences.at[i, 'sent'] = word_line
        return sentences
