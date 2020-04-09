import pandas as pd 
import os 
from glob import glob
import re

path = os.getcwd()
csv_files = glob('*.csv')

dates = [(re.findall(r'((?:\d+\.\d+\.\d+))', csv)) for csv in csv_files]
for date in dates:
    matching_pair = [date]
    excluded_list = list(dates)
    excluded_list.remove(date)
    for item in matching_pair:
        if item in excluded_list:
            print(item, excluded_list[excluded_list == item])
print(dates)
