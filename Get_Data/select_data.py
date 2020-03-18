import pandas as pd 
import numpy as np 
from datetime import datetime as dt 
import glob
import re
import os

#dates need to be in mm.dd.yyyy format
d_start = '01.31.2019'
d_end = '04.25.2019'

re_for_start = d_start[-4:]+ '-' +d_start[:2] +'-'+ d_start[3:5]
re_for_end = d_end[-4:]+ '-' +d_end[:2] +'-'+ d_end[3:5]
print(re_for_start)
print()
print(re_for_end)

dt_start = dt.strptime(d_start, '%m.%d.%Y')
dt_end = dt.strptime(d_end, '%m.%d.%Y')

#find a file that has these dates between its start and end dates
file = os.path.join(os.getcwd(), os.listdir(os.getcwd())[0])
path = os.path.dirname(file)
all_csv = glob.glob(path + '/*.csv')

date_range_regex = re.compile(r'\d{2}.\d{2}.\d{4}_\d{2}.\d{2}.\d{4}')
date_ranges = [[],[],[]]

for item in all_csv:
    mo = date_range_regex.search(item)
        
    date_ranges[0].append(str(item)[-39:])
    date_ranges[1].append(mo.group()[:10])
    date_ranges[2].append(mo.group()[11:])

filename = date_ranges[0][:]
start_date = date_ranges[1][:]
end_date = date_ranges[2][:]

if not filename:
    print('No files in this directory')

for i, (start, end) in enumerate(zip(start_date, end_date)):
    d1 = dt.strptime(start, '%m.%d.%Y')
    d2 = dt.strptime(end, '%m.%d.%Y')
    if (d1 < dt_start) and (d2 > dt_end):
        usable_file = filename[i]
        print('Usable file found ' +usable_file)
        break
    elif i == len(start_date) - 1:
        print('No usable files')

if not usable_file:
    print('No file for the given start and end dates')
    exit()

df = pd.read_csv(usable_file)
new_df = df[(df['created_utc'] >= re_for_start) & (df['created_utc'] <= re_for_end)]
new_filename = usable_file[:14] +str(d_start)+ '_' +str(d_end)+ '.csv'
new_df.to_csv(new_filename, index=False)
print(new_filename + ' Added!')