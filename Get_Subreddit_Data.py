import pandas as pd
import requests
from datetime import datetime
import time
import csv
import os

# Class for getting subreddit data via pushift.io api
class Get_Data:
    '''
    Get_data(subreddit, start_date, end_date) is a method that gets data from the
    pushift.io api and organizes it into a dataframe, sorted by date, and exports
    this data to a csv file for later manipulation.

    Parameters:
        subreddit (string) : a string that represents the subreddit data you want to
            get, so for example the r/politics titles and data would have a 
            subreddit = \'politics\'

        start_date (string) : string that represents the first day of posts to be saved
            Must be in the \'mm.dd.YYYY\' format.

        end_date (string) : string that represents the last day of posts to be saved.
            Must be in the \'mm.dd.YYYY\' format.
    '''
    def __init__(self, subreddit, start_date, end_date):
        self.subreddit = subreddit
        self.start_date = start_date
        self.end_date = end_date
        filename = subreddit+ '_data_' +str(start_date)+ \
            '_' +str(end_date)+ '.csv'
        self.filename = 'Get_Data\\' + filename
        self.check_for_existing_data()

    def check_for_existing_data(self):
        '''
        Method that finds if a file was already started with the desired dates,
        and if so restarts the data gathering process so that if data gathering was
        aborted unexpectedly you can restart it without issue.

        Parameters:

            None
        '''
        if os.path.isfile(self.filename):
            df = pd.read_csv(self.filename)
            last_time = df['created_utc'].iloc[-1]
            start = pd.Timestamp(str(last_time)).value // 10**9
            print('file found, adding to data')
            self.get_subreddit_titles(start, self.end_date)

        else:
            print('No file found, starting new export of data')
            self.get_subreddit_titles(self.start_date, self.end_date)

    def get_subreddit_titles(self, start_date, end_date):
        '''
        Main method for getting subreddit data from the pushift.io api and adding 
        it to a pandas dataframe, and after it is done, exporting it to a csv file.

        Parameters:

            start_date (string) : string that represents the first day of posts to be saved
                Must be in the \'mm.dd.YYYY\' format.

            end_date (string) : string that represents the last day of posts to be saved.
                Must be in the \'mm.dd.YYYY\' format.
        '''
        subreddit = self.subreddit
        filename = self.filename
        start = start_date
        if isinstance(start_date, str):
            start = int(time.mktime(datetime.strptime(start_date, "%m.%d.%Y").timetuple())) 
        end = int(time.mktime(datetime.strptime(end_date, "%m.%d.%Y").timetuple()))
        x = 1
        while True:
            #difference = end - start
            url = 'https://api.pushshift.io/reddit/search/submission/?before='+ str(end)+ '&after=' + str(start) + '&subreddit='+ subreddit
            print(url)
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
