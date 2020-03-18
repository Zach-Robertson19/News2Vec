import tensorflow as tf 
import pandas as pd 
from langdetect import detect
from langdetect import DetectorFactory 
import numpy as np
import string
import re


#function that takes a list of sentence strings and turns them into an 
#array of the sentences split into seperate words and punctuation
def word_array(df, sent=True):
    DetectorFactory.seed = 0 

    
    for i, line in enumerate(df):
        try:
            if detect(line) != 'en':
                del df[i]
        except:
            continue    
    word_list = []
    words = 0

    for line in df:
        
        word_line = []
        word_line_punct = list(re.split(r'\s+', line))

        for word in word_line_punct:
            word_punct = list(filter(None, re.split(r'(^(?:[A-Z]*[a-z]+\'[s])|^(?:[A-Z]*[a-z]+[s]\')|^(?:[A-Z]\.){1,2}|[,.;:!?\'\"])', word)))
            for elem in word_punct:
                if elem in string.punctuation:
                    pass
                else:
                    if sent:
                        word_line.append(elem.lower())
                    else:
                        word_list.append(elem.lower())
                    words += 1
        if sent:   
            word_list.append(word_line)
    return word_list

def pkl(filename, sent):
    data = pd.read_csv(filename)
    df = data['title']

    words = word_array(df, sent)
    pkl = pd.Series(words)
    if sent:
        pkl_filename = str(filename)[:-4] + '_sent.pkl'
    else:
        pkl_filename = str(filename)[:-4] + '_nosent.pkl'
    pkl.to_pickle(pkl_filename)
    print('pkl file added')

df = pd.read_csv('Data/politics_data_11.22.2018_11.23.2018.csv')
df = df['title']
print(word_array(df))