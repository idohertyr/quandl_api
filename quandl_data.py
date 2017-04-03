"""
Author: Ian Doherty - idohertyr
Date: March 31, 2017

This program uses Quandl API to retrieve settle and close prices for
The S&P 500 Volatility Futures. Then formatted and exported to an CSV.

"""

import quandl
import pandas as pd
from time import sleep
from api_key import *

quandl.ApiConfig.api_key = api_key

# Constants
settle_col = 5
close_col = 4

# Main DataFrame
prices = pd.DataFrame()

# Count used to prevent too many api calls
api_count = 0

# Count the current contract to show progress.
contract_count = 0

# Contract Names 148
contracts = ["VXK2004",
"VXM2004",
"VXN2004",
"VXQ2004",
"VXU2004",
"VXV2004",
"VXX2004",
"VXF2005",
"VXG2005",
"VXH2005",
"VXK2005",
"VXM2005",
"VXQ2005",
"VXV2005",
"VXX2005",
"VXZ2005",
"VXF2006",
"VXG2006",
"VXH2006",
"VXJ2006",
"VXK2006",
"VXM2006",
"VXN2006",
"VXQ2006",
"VXU2006",
"VXV2006",
"VXX2006",
"VXZ2006",
"VXF2007",
"VXG2007",
"VXH2007",
"VXJ2007",
"VXK2007",
"VXM2007",
"VXN2007",
"VXQ2007",
"VXU2007",
"VXV2007",
"VXX2007",
"VXZ2007",
"VXF2008",
"VXG2008",
"VXH2008",
"VXJ2008",
"VXK2008",
"VXM2008",
"VXN2008",
"VXQ2008",
"VXU2008",
"VXV2008",
"VXX2008",
"VXZ2008",
"VXF2009",
"VXG2009",
"VXH2009",
"VXJ2009",
"VXK2009",
"VXM2009",
"VXN2009",
"VXQ2009",
"VXU2009",
"VXV2009",
"VXX2009",
"VXZ2009",
"VXF2010",
"VXG2010",
"VXH2010",
"VXJ2010",
"VXK2010",
"VXM2010",
"VXN2010",
"VXQ2010",
"VXU2010",
"VXV2010",
"VXX2010",
"VXZ2010",
"VXF2011",
"VXG2011",
"VXH2011",
"VXJ2011",
"VXK2011",
"VXM2011",
"VXN2011",
"VXQ2011",
"VXU2011",
"VXV2011",
"VXX2011",
"VXZ2011",
"VXF2012",
"VXG2012",
"VXH2012",
"VXJ2012",
"VXK2012",
"VXM2012",
"VXN2012",
"VXQ2012",
"VXU2012",
"VXV2012",
"VXX2012",
"VXZ2012",
"VXF2013",
"VXG2013",
"VXH2013",
"VXJ2013",
"VXK2013",
"VXM2013",
"VXN2013",
"VXQ2013",
"VXU2013",
"VXV2013",
"VXX2013",
"VXZ2013",
"VXF2014",
"VXG2014",
"VXH2014",
"VXJ2014",
"VXK2014",
"VXM2014",
"VXN2014",
"VXQ2014",
"VXU2014",
"VXV2014",
"VXX2014",
"VXZ2014",
"VXF2015",
"VXG2015",
"VXH2015",
"VXJ2015",
"VXK2015",
"VXM2015",
"VXN2015",
"VXQ2015",
"VXU2015",
"VXV2015",
"VXX2015",
"VXZ2015",
"VXF2016",
"VXG2016",
"VXH2016",
"VXJ2016",
"VXK2016",
"VXM2016",
"VXN2016",
"VXQ2016",
"VXU2016",
"VXV2016",
"VXX2016",
"VXZ2016",
"VXF2017",
"VXG2017",
"VXH2017"]

# Number of contracts
num_of_contracts = len(contracts)

for contract in contracts:
    # Count current contract
    contract_count += 1

    print ('Working on ' + str(contract_count) + '/' + str(num_of_contracts))

    # Collect Data / Only 20 calls every 10 minutes
    settle_data = quandl.get("CBOE/" + str(contract) + "." + str(settle_col))
    api_count += 1
    close_data = quandl.get("CBOE/" + str(contract) + "." + str(close_col))
    api_count += 1

    print contract

    print type(contract)

    # Concat Data
    contract_data = pd.concat([settle_data, close_data], axis=1)
    contract_data['Contract'] = contract

    # If prices is empty, set equal to first data set.
    if(prices.size <= 0):
        prices = contract_data

    # Add contract_data
    prices = prices.append(contract_data)

    # Check api_count
    if(api_count >= 20):
        sleep(600)
        api_count = 0

    print 'printing data: '
    print prices

print ('Size of data: ' + str(prices.size))

print ('Exporting to CSV file.')

# Export data to CSV file.
prices.to_csv('./data/vix_futures.csv')

print ('Exporting to Excel File.')

# Export data to Excel file.
prices.to_excel('./data/vix_futures.xlsx', sheet_name='VIX Futures Prices')

print ('Complete!')