import pandas as pd
import glob
import re
import os
import numpy as np

Remove = False

path = r'C:\Users\Zach\Documents\News2vec\Get_data'
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

check = end_date[0]
seq = []
x = 0
while True:
    if check in start_date:
        check_filename = filename[end_date.index(check)]
        start_date_filename = filename[start_date.index(check)]
        check = end_date[start_date.index(check)]
        if check_filename not in seq:
            seq.append(check_filename)
        seq.append(start_date_filename)
        x += 1
    elif x >= (len(start_date)-1):
        break
    else:
        x += 1
        check = end_date[x]

final = []
for item in seq:
    seq_index = seq.index(item)
    if seq_index >= len(seq) - 1:
        break
    next_seq = seq[seq_index + 1]
    filename_index = filename.index(item)
    next_filename_index = filename.index(next_seq)
    if end_date[filename_index] != start_date[next_filename_index]:
        final.append(seq[:seq_index+1])
        seq = [x for x in seq if x not in seq[:seq_index+1]]
      
final.append(seq)
print(filename)
for item in final:
    first_item = item[0]
    last_item = item[-1]
    start_date_item = start_date[filename.index(first_item)]
    end_date_item = end_date[filename.index(last_item)]
    filename_new = item[0][:14] \
        +str(start_date_item)+ '_' \
            +str(end_date_item)+ '.csv'
    df = pd.DataFrame()
    for j in item:
        df_j = pd.read_csv(j)
        df = pd.concat([df, df_j])
    df.to_csv(filename_new, index=False)

    print(filename_new + ' Added')
