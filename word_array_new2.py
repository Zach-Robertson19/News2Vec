import pandas as pd 
from langdetect import detect
from langdetect import DetectorFactory 
import numpy as np
from urllib.parse import urlparse
import re
import pickle

#function that takes a list of sentence strings and turns them into an 
#array of the sentences split into seperate words and punctuation
def word_array(csv_filename, pkl=True):
    df  = pd.read_csv(csv_filename)
    DetectorFactory.seed = 0 

    
    sentences = pd.DataFrame(columns=['title', 'sent', 'url'])
    words = 0

    for i, (title, url) in enumerate(zip(df['title'], df['url'])):
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
        

    pick_filename = str(csv_filename)[:-4] + '_sent.pkl'
    #pickle the word list
    if pickle:
        sentences.to_pickle(pick_filename)
        print(f'Pickle file added {pick_filename}')
    return sentences



def read_pick(pick_filename):
    df = pd.read_pickle(pick_filename)
    return df


sent = word_array('politics_data_11.21.2018_10.10.2019.csv', pkl=False)
print(sent)
