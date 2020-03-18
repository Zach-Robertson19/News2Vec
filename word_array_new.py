import pandas as pd 
from langdetect import detect
from langdetect import DetectorFactory 
import numpy as np

import re
import pickle

#function that takes a list of sentence strings and turns them into an 
#array of the sentences split into seperate words and punctuation
def word_array(csv_filename, sent=True, pkl=True):
    df  = pd.read_csv(csv_filename)
    df = df['title']
    DetectorFactory.seed = 0 

    
    word_list = []
    words = 0

    for i, line in enumerate(df):
        try:
            if detect(line) != 'en':
                del df[i]
        except:
            pass
        word_line = []
        word_line_punct = list(re.split(r'\s+', line))

        for word in word_line_punct:
            word_punct = list(filter(None, re.split(r'(^(?:[A-Z]*[a-z]+\'[st])|^(?:[A-Z]*[a-z]+[s]\')|^(?:[A-Z]\.){1,2}|[^a-zA-Z])', word)))
            for elem in word_punct:
                punct_match = re.match(r'[^a-zA-Z0-9]', elem)
                if punct_match != None:
                    pass
                else:
                    if sent:
                        word_line.append(elem.lower())
                    else:
                        word_list.append(elem.lower())
                    words += 1
        if sent:   
            word_list.append(word_line)
    if sent:
        pick_filename = str(csv_filename)[:-4] + '_sent.pkl'
    else:
        pick_filename = str(csv_filename)[:-4] + '_nosent.pkl'
        #pickle the word list
    if pickle:
        with open(pick_filename, 'wb') as f:
            pickle.dump(word_list, f)
            print('Pickle file added', pick_filename)
        
    return word_list

words = pd.read_csv('politics_data_11.21.2018_10.10.2019.csv')
print(words['title'][-4:])
print()
print(words['url'][-4:])
print()
print(words['permalink'][-4:])