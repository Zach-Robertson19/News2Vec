import pandas as pd
import requests
from datetime import datetime
import time
import csv
import os

''' 
get_subreddit_titles() is a function that gives you various data for the chosen subreddit
over a chosen time period, the actual data is specified in the column_names variable
and can be changed if you know the names of the perameters returned in 
the request object with is not hard to do given the example here.

get_subreddit_titles() takes 3 arguments

(subreddit) is the name of the subreddit as a string without r/, capitalization matters. E.g. r/politics
is 'politics'

(start_date, end_date) are the start and end dates in the mm.dd.YYYY format
'''

def get_subreddit_titles(subreddit, start_date, end_date):
    start = int(time.mktime(datetime.strptime(start_date, "%m.%d.%Y").timetuple())) 
    end = int(time.mktime(datetime.strptime(end_date, "%m.%d.%Y").timetuple()))

    filename = subreddit+ '_data_' +str(start_date)+ \
        '_' +str(end_date)+ '.csv'
    
    x = 1
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        last_time = df['created_utc'].iloc[-1]
        start = pd.Timestamp(str(last_time)).value // 10**9
        
    while True:
        #difference = end - start
        '''if difference < 10:
            print('All Done!')
            break'''
  
        url = 'https://api.pushshift.io/reddit/search/submission/?before='+ str(end)+ '&after=' + str(start) + '&subreddit='+ subreddit

        r = requests.get(url)
        try:
            data = r.json()
        except:
            print('No data')
            pass
        if not data['data']:
            print('All Done!')
            break
        arr = []

        for item in data['data']:
            column_names = ['created_utc', 'id', 'permalink', \
                'score', 'selftext', \
                    'title', 'subreddit', \
                        'url']
            try:
                arr_new = [pd.to_datetime(item['created_utc'], unit='s'), \
                    item['id'], item['permalink'], item['score'], \
                        item['selftext'], item['title'], item['subreddit'], \
                            item['url']]
            except:
                pass
                
            arr.append(arr_new)
            print(str(x), pd.to_datetime(item['created_utc'], unit='s'), \
                item['title'])
            start = item['created_utc']
            x += 1
        
        df = pd.DataFrame(arr)
        
        if not os.path.isfile(filename):
            df.to_csv(filename, header=column_names, index=False)
        
        else: 
            old_csv = pd.read_csv(filename)
            old_df = pd.DataFrame(old_csv)
            new_df = df[~df[1].isin(old_df['title'])]
            if new_df.empty:
                print('Nothing Added!')
            new_df.to_csv(filename, mode='a', header=False, index=False)
        
        time.sleep(1)
        
get_subreddit_titles('politics', '11.21.2018', '03.02.2020')
