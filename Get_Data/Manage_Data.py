import pandas as pd 
from datetime import datetime as dt
import re
import os

# Class to make a subset of data from a larger set of data
class Get_Subset_of_Data:
    '''
    Class that searches for an existing file whos dates contain the given dates in
    initialized class, then cuts that file to only the desired dates and exports that
    data to a new file.

    Parameters:

        start_date (string) : string that represents the first day of posts to be saved
            Must be in the \'mm.dd.YYYY\' format.

        end_date (string) : string that represents the last day of posts to be saved.
            Must be in the \'mm.dd.YYYY\' format.
    '''

    def __init__(self, start_date, end_date):
        self.start_date, self.end_date = start_date, end_date
        self.dt_start = dt.strptime(start_date, '%m.%d.%Y')
        self.dt_end = dt.strptime(end_date, '%m.%d.%Y')
        dates = self.get_csv_file_dates()
        dates_dict = self.split_dates_from_dict(dates)
        self.check_date_ranges(dates_dict)

    def get_csv_file_dates(self):
        '''
        Method that gets the dates related to the csv files from their titles.

        Parameters:

            None
        '''
        data = []
        date_range_regex = re.compile(r'\d{2}.\d{2}.\d{4}_\d{2}.\d{2}.\d{4}')
        dates = dict()
        for item in os.listdir():
            if item[-3:] == 'csv':
                data.append(item)
                date = re.search(date_range_regex, item)[0]
                dates[item] = date
        return dates

    def split_dates_from_dict(self, dates):
        '''
        Method that creates a dictionary of each data file that defines the start 
        and end dates for each file for easier matching.

        Parameters:
            
            dates (dict) : dictionary containing the filename and date_ranges of 
                each data file in the directory. Created from get_csv_file_dates().
        '''
        dates_dict = dict()
        for i, (key, value) in enumerate(dates.items()):
            sep_dates = value.split('_')
            dates_dict[i] = dict(zip(['start', 'end'], sep_dates))
            dates_dict[i]['filename'] = key
        return dates_dict

    def check_date_ranges(self, dates_dict):
        '''
        Method that finds if a file exists that contains the given dates.

        Parameters:

            dates_dict (dict) : a dictionary containing the filename, start and end
                date for each data file in the directory, created from 
                split_dates_from_dict(dates) where the dates variable is created
                in the get_csv_files_dates()
        '''
        for _, value in dates_dict.items():
            check_start = value['start']
            check_end = value['end']
            dt_check_start = dt.strptime(check_start, '%m.%d.%Y')
            dt_check_end = dt.strptime(check_end, '%m.%d.%Y')
            if dt_check_start <= self.dt_start and dt_check_end >= self.dt_end:
                print('File found!')
                self.filename = value['filename']
                self.cut_csv_data(self.filename)
                break

    def cut_csv_data(self, filename):
        '''
        Method that makes the subset of the data from the file found during the loop
        in check_date_ranges(dates_dict), and exports it to a csv file.

        Parameters:

            filename (string) : filename that the data is coming from, so the larger
                full set of data.
        '''
        data = pd.read_csv(filename, header=0)
        data = data[(data['created_utc'] >= str(self.dt_start)) & (data['created_utc'] <= str(self.dt_end))]
        subreddit = self.filename.split('_')[0]
        cut_filename = subreddit + '_' + 'data' + '_' + self.start_date + '_' + self.end_date + '.csv'
        data.to_csv(cut_filename, index=False)
        print(f'{cut_filename} added to directory')

# Class that adds data with matching dates
class Add_Data_from_Matching_Dates:
    '''
    Class that searches for date matches in the data files, then adds them
    together and exports it as a new data set.

    Parameters:

        None
    '''
    def __init__(self):
        dates = self.get_csv_file_dates()
        dates_dict = self.split_dates_from_dict(dates)
        self.check_for_date_matches(dates_dict)

    def get_csv_file_dates(self):
        '''
        Method that gets the dates related to the csv files from their titles.

        Parameters:

            None
        '''
        data = []
        date_range_regex = re.compile(r'\d{2}.\d{2}.\d{4}_\d{2}.\d{2}.\d{4}')
        dates = dict()
        for item in os.listdir():
            if item[-3:] == 'csv':
                data.append(item)
                date = re.search(date_range_regex, item)[0]
                dates[item] = date
        return dates

    def split_dates_from_dict(self, dates):
        '''
        Method that creates a dictionary of each data file that defines the start 
        and end dates for each file for easier matching.

        Parameters:
            
            dates (dict) : dictionary containing the filename and date_ranges of 
                each data file in the directory. Created from get_csv_file_dates().
        '''
        dates_dict = dict()
        for i, (key, value) in enumerate(dates.items()):
            sep_dates = value.split('_')
            dates_dict[i] = dict(zip(['start', 'end'], sep_dates))
            dates_dict[i]['filename'] = key
        return dates_dict

    def check_for_date_matches(self, dates_dict):
        '''
        Method that finds matches between start and end dates in dates_dict provided
        by the split_dates_from_dict(dates) method, then adds that data together
        and exports it to a new file

        Parameters:

            dates_dict (dict) : dictionary produced by split_dates_from_dict(dates)  
        '''
        for key, value in dates_dict.items():
            other_keys = [item for item in list(dates_dict.keys()) if item != key]
            other_dates_dict = {key: dates_dict[key] for key in dates_dict.keys() & other_keys}
            for _, value2 in other_dates_dict.items():
                if value['end'] == value2['start']:
                    df1 = pd.read_csv(value['filename'])
                    df2 = pd.read_csv(value2['filename'])
                    df_final = pd.concat([df1, df2])
                    new_filename_group = value['filename'].split('_')
                    new_filename = '_'.join(new_filename_group[:3]) + '_' + value2['end'] + '.csv'
                    df_final.to_csv(new_filename, index=False)
                    print(f'{new_filename} added to directory.')
