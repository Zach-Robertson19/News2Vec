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

df = pd.read_pickle('politics_data_11.21.2018_10.10.2019_sent.pkl')

def build_set(words, n_words):
    words = [item for sublist in words for item in sublist]
    most_occur = [['UNK', -1]]
    most_occur.extend(Counter(words).most_common(n_words))


    dictionary = dict()
    data = list()

    for word, _ in most_occur:
        dictionary[word] = len(dictionary)

    unk_words = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]
        else:
            index = 0
            unk_words += 1
        data.append(index)
    most_occur[0][1] = unk_words
    reversed_dict = dict(zip(dictionary.values(), dictionary.keys()))

    return data, most_occur, dictionary, reversed_dict

def TDIDF(sent_words):
    rawcount_dict = dict(Counter(chain.from_iterable(sent_words)))
    '''with open('training_sent_dict.pickle', 'wb') as handle:
        pickle.dump(rawcount_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)'''
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

def create_model(words, model_name):
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

def read_model(model_name):
    model = gensim.models.KeyedVectors.load_word2vec_format(model_name + '.bin', binary=True)
    return model

def TDIDFSentenceVecotrs(model_name, sent_words):
    model = read_model(model_name)
    _, TF_dict = TDIDF(sent_words)
    sent_vectors =[]
    sentences = []
    for item in sent_words:
        weights = []
        w2v_vectors = []
        weighted_vectors = []

        for i in item:
            word_vector = model[i]
            weight = TF_dict[i]
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
    return sent_vector_dict

def CosineSimilarity(sent_vector_dict, sent1, sent2) :
    print(sent1, sent2)
    vector1 = sent_vector_dict[sent1]
    vector2 = sent_vector_dict[sent2]
    print(vector1, vector2)
    dot_product = np.dot(vector1, vector2)
    mag1 = np.linalg.norm(vector1)
    mag2 = np.linalg.norm(vector2)

    cos_sim = dot_product / (mag1*mag2)
    return cos_sim


words = df['sent'].to_list()


vector = TDIDFSentenceVecotrs('politics_data_11.21.2018_10.10.2019_W2VModel', words)

cos = CosineSimilarity(vector, list(vector.keys())[0], list(vector.keys())[1])
print(cos)



#dict_list, TF_dict = TDIDF(words)
#new_list = sorted(TF_dict, key=TF_dict.get, reverse=True)[:100]

