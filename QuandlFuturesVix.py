"""A demonstration of Quandl Api.

Author: Ian Doherty
Date: March 31, 2017

This program uses the quandl API to retrieve information for
The S&P 500 Volatility Futures and VIX Index. The results are then exported to an CSV and Excel.

** requires api api_key file!
Quandl allows 20 calls every 10 minutes for free.

Returns: pandas.DataFrame
    Columns: [Trade Date, Settle, Close, Contract Name, VIX Close]
"""


"""Import all at top of module."""
import pandas as pd
import time
import quandl
from api_key import *

"""Set Api key"""
quandl.ApiConfig.api_key = api_key

class QuandlFuturesVix:
    """Combines columns: 'Settle', 'Close', and 'VIX Close'
    
    """
    def __init__(self, key):
        self.key = key
        self.contracts = [
            #"VXF2004","VXG2004","VXH2004","VXJ2004","VXK2004","VXM2004","VXN2004","VXQ2004","VXU2004","VXV2004","VXX2004","VXZ2004",
            #"VXF2005","VXG2005","VXH2005","VXJ2005","VXK2005","VXM2005","VXH2005","VXQ2005","VXU2005","VXV2005","VXX2005","VXZ2005",
            #"VXF2006","VXG2006","VXH2006","VXJ2006","VXK2006","VXM2006","VXN2006","VXQ2006","VXU2006","VXV2006","VXX2006","VXZ2006",
            #"VXF2007","VXG2007","VXH2007","VXJ2007","VXK2007","VXM2007","VXN2007","VXQ2007","VXU2007","VXV2007","VXX2007","VXZ2007",
            #"VXF2008","VXG2008","VXH2008","VXJ2008","VXK2008","VXM2008","VXN2008","VXQ2008","VXU2008","VXV2008","VXX2008","VXZ2008",
            #"VXF2009","VXG2009","VXH2009","VXJ2009","VXK2009","VXM2009","VXN2009","VXQ2009","VXU2009","VXV2009","VXX2009","VXZ2009",
            #"VXF2010","VXG2010","VXH2010","VXJ2010","VXK2010","VXM2010","VXN2010","VXQ2010","VXU2010","VXV2010","VXX2010","VXZ2010",
            #"VXF2011","VXG2011","VXH2011","VXJ2011","VXK2011","VXM2011","VXN2011","VXQ2011","VXU2011","VXV2011","VXX2011","VXZ2011",
            #"VXF2012","VXG2012","VXH2012","VXJ2012","VXK2012","VXM2012","VXN2012","VXQ2012","VXU2012","VXV2012","VXX2012","VXZ2012",
            #"VXF2013","VXG2013","VXH2013","VXJ2013","VXK2013","VXM2013","VXN2013","VXQ2013","VXU2013","VXV2013","VXX2013","VXZ2013",
            #"VXF2014","VXG2014","VXH2014","VXJ2014","VXK2014","VXM2014","VXN2014","VXQ2014","VXU2014","VXV2014","VXX2014","VXZ2014",
            #"VXF2015","VXG2015","VXH2015","VXJ2015","VXK2015","VXM2015","VXN2015","VXQ2015","VXU2015","VXV2015","VXX2015","VXZ2015",
            #"VXF2016","VXG2016","VXH2016","VXJ2016","VXK2016","VXM2016","VXN2016","VXQ2016","VXU2016","VXV2016","VXX2016","VXZ2016",
            "VXF2017","VXG2017","VXH2017","VXJ2017","VXK2017"
        ]
        self.api_call_count = 1
        self.contract_count = 0
        self.contract_data = pd.DataFrame()
        self.vix_data = pd.DataFrame()
        self.complete_data = pd.DataFrame()
        pass

    def get_futures_prices(self):
        """Returns settle and close columns

        :rtype: pandas.core.frame.DataFrame
        """
        for contract in self.contracts:
            self.contract_count += 1

            print ('Working on ' + str(self.contract_count) + '/' + str(len(self.contracts)))

            contract_data = quandl.get("CBOE/" + str(contract))
            self.api_call_count += 1

            settle_col = contract_data['Settle']
            close_col = contract_data['Close']

            amend_col = pd.concat([settle_col, close_col], axis=1)

            amend_col['Contract'] = contract

            if self.complete_data.size == 0:
                self.complete_data = amend_col
            else:
                self.complete_data = self.complete_data.append(amend_col)

            self.check_api_calls()
        pass

    def get_vix_data(self):
        """Returns CBOE Vix Index Close Price Column.
        
        :rtype: pandas.core.series.Series
        """
        print('Getting vix data...')
        vix_data = quandl.get("CBOE/VIX")
        vix_data = vix_data['VIX Close']
        self.vix_data = vix_data
        pass

    def write_to_files(self):
        """Writes combined data to CSV and Excel files ('./data').
        
        """
        print ('Writing to Files ..')
        time_str = time.strftime('%Y%m%d')
        self.complete_data.index.name = 'Trade Date'
        self.complete_data.to_csv('./data/' + time_str + '_quandl_futures_vix.csv',
                                  index=True)
        self.complete_data.to_excel('./data/' + time_str + '_quandl_futures_vix.xlsx',
                                    sheet_name='VIX Futures Prices',
                                    index=True)
        print 'Complete!'
        pass

    def print_class(self):
        """Prints information about the QuandlFuturesVix class.
        
        """
        print('{}'.format(self.complete_data))
        pass

    """TODO: Clean data."""
    def clean_data(self, data):
        """Cleans data sets.
        
        Args:
            data (pandas.Series): Data to be cleaned.
        :rtype: pandas.Series
        """
        pass

    def create_contract_column(self, rows, value):
        """Returns a column of data filled with contract name
        
        """
        return pd.Series(value for _ in range(0, rows))
        pass

    def check_api_calls(self):
        """Helps avoid too many Api calls.
        
        """
        if self.api_call_count >= 20:
            time.sleep(600)
            self.api_call_count = 0
        pass

    def combine_futures_vix(self):
        """Returns future columns and vix close combined
        
        """
        self.complete_data = pd.merge(self.complete_data,
                                      pd.DataFrame(self.vix_data),
                                      how='inner',
                                      left_index=True,
                                      right_index=True
                                      )
    pass

vix = QuandlFuturesVix(api_key)
vix.get_futures_prices()
vix.get_vix_data()
vix.combine_futures_vix()
vix.write_to_files()
