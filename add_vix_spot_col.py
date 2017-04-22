"""
Author: Ian Doherty - idohertyr
Data: April 22, 2017

This script adds the Vix Index spot price to the existing data pulled
from the 'quandl_data.py' named './data/vix_futures.csv'

Inputs: 2 files:
1. './data/vix_futures_combined.csv'
2. './existing_data/CBOE-VIX-CLOSE.csv'

Output: 1 File:
1. './data/complete_table.csv'
    and './data/{datestr}futures_vix_spot.xlsx'

"""

import pandas as pd
import time

# Import CSV files
futures = pd.read_csv('./data/vix_futures_combined.csv')
vix_spot = pd.read_csv('./existing_data/CBOE-VIX-CLOSE.csv')

'''
LEFT JOIN FUTURES <- VIX INDEX SPOT
'''
def left_join_dataframes(left, right):
    # Print input sizes
    print ('LEFT SIZE' + str(left.size))
    print ('RIGHT SIZE' + str(right.size))

    # Perform Join and print result
    result = pd.merge(futures, vix_spot, on='Date', how='left')
    print ('RESULT SIZE' + str(result.size))

    # print and return result
    print result
    return result

'''
DROP DUPLICATE ROWS
'''
def remove_duplicates(data):
    print ('Before dropping duplicate rows: ' + str(data.size))
    # Used to check for duplicate rows
    data = data.drop_duplicates()
    print ('After dropping duplicate rows: ' + str(data.size))
    return data

'''
WRITE TO FILE
'''
def write_files(data):
    print ('Writing to Files ..')
    timestr = time.strftime('%Y%m%d')
    data.to_csv('./data/' + timestr + 'futures_vix_spot.csv', index=False)
    data.to_excel('./data/' + timestr + 'futures_vix_spot.xlsx', index=False)
    print 'Complete'

'''
DEFINE TIME STAMP
'''

'''
EXECUTE
'''
data = left_join_dataframes(futures, vix_spot)
data = remove_duplicates(data)
data = write_files(data)
