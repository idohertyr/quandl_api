"""
Author: Ian Doherty - idohertyr
Data: April 1, 2017

This python script updates the data and appends new data.

"""

import pandas as pd

old_prices = pd.read_csv('./existing_data/vix_futures_old.csv')
new_prices = pd.read_csv('./existing_data/vix_futures_new.csv')

print ('Old Price CSV file size: ' + str(old_prices.size))
print ('New Price CSV file size' + str(new_prices.size))

print ('Total: ' + str(old_prices.size + new_prices.size))

appended_list = old_prices.append(new_prices)

appended_list = appended_list.sort_values(by='Trade Date')

print ('New CSV file size: ' + str(appended_list.size))

print ('Writing to Files ..')
appended_list.to_csv('./data/vix_futures_combined.csv', index=False)
appended_list.to_excel('./data/vix_futures_combined.xlsx', index=False)

print 'Complete'