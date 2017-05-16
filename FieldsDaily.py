"""Collects data for an assortment of Volatility Indexes.

Author: Ian Doherty
Date: May 15, 2017

This program uses the quandl API to retrieve information for:

The following all have DateTime indexes.
    
    Data analysis taken on May 16, 2017
    
    CBOE/VXST: (CBOE Short-Term Volatility Index)
        ** Measure of 9 day IV of (SPX) Index options. **
        High: 2013-11-19 -> 2017-05-15
        Open: 2013-11-19 -> 2017-05-15
        Low: 2013-11-19 -> 2017-05-15
        Close: 2011-01-03 -> 2017-05-15
    CBOE/VIX: (CBOE Volatility Index)
        ** Measure of 30 day IV of (SPX) Index options. **
        High: 2007-12-04 -> 2017-05-15
        Open: 2007-12-04 -> 2017-05-15
        Low: 2007-12-04 -> 2017-05-15
        Close: 2007-12-04 -> 2017-05-15
    CBOE/VXV: (CBOE 3-Month Volatility Index)
        ** Measure of 3-month IV of (SPX) Index options. **
        Open: 2007-12-04 -> 2017-05-15
        High: 2007-12-04 -> 2017-05-15
        Low: 2007-12-04 -> 2017-05-15
        Close: 2007-12-04 -> 2017-05-15 CLOSE??
    CHRIS/CBOE_VX1: (Continuous Contract #1)
        ** Front Month **
        Open: 2005-06-20 -> 2017-05-12
        High: 2005-06-20 -> 2017-05-12
        Low: 2005-06-20 -> 2017-05-12
        Close: 2005-06-20 -> 2017-05-12
        Settle: 2005-06-20 -> 2017-05-12
        Change: 2005-06-20 -> 2017-05-12
        Total Volume: 2005-06-20 -> 2017-05-12
        EFP: 2005-06-20 -> 2017-05-12
        Prev. Day Open Interest: 2005-06-20 -> 2017-05-12
    CHRIS/CBOE_VX2: (Continuous Contract #2)
        Open: 2005-11-17 -> 2017-05-15
        High: 2005-11-17 -> 2017-05-15
        Low: 2005-11-17 -> 2017-05-15
        Close: 2005-11-17 -> 2017-05-15
        Settle: 2005-11-17 -> 2017-05-15
        Change: 2005-11-17 -> 2017-05-15
        Total Volume: 2005-11-17 -> 2017-05-15
        EFP: 2005-11-17 -> 2017-05-15
        Prev. Day Open Interest: 2005-11-17 -> 2017-05-15
    CBOE/VXMT: (CBOE Mid-Term Volatility Index)
        ** Measure of 6-month IV of (SPX) Index options. **
        Open: 2013-11-27 -> 2017-05-15
        High: 2013-11-27 -> 2017-05-15
        Low: 2013-11-27 -> 2017-05-15
        Close: 2008-01-07 -> 2017-05-15
    -- Not implemented yet ----------------------------------
    VIXMO: (VIX Month Only)
        ** Measure of 30 day IV of (SPX) Index options, using SPX monthly options. **
        Open:
        High:
        Low:
        Close:

    **Each one returns a pandas.DataFrame

** requires api api_key file!
Quandl allows 20 calls every 10 minutes for free.

Returns: 2 Files

"""

"""Import all at top of module."""
import pandas as pd
import time
import quandl
from api_key import *

"""Set API key"""
quandl.ApiConfig.api_key = api_key

class FieldsDaily:
    """Collects data for Volatility Indexes and writes to file.
    
    """
    def __init__(self):
        self._indexes = [
            "CBOE/VXST",
            "CBOE/VIX",
            "CBOE/VXV",
            "CHRIS/CBOE_VX1",
            "CHRIS/CBOE_VX2",
            "CBOE/VXMT"
        ]
        self.count = 0
        self.api_call_count = 0
        self.complete_data = pd.DataFrame()
        pass

    def get_index_data(self):
        """Collects and combines data for defined indexes.
        
        :return: 
        """
        for _index in self._indexes:
            self.count += 1

            print ('Working on ' + str(_index) + ' of ' + str(len(self._indexes)))

            data = quandl.get(str(_index))

            if _index == 'CBOE/VIX':
                self.write_single_to_file(data['VIX Close'], _index[_index.index('/')+1:])
                self.complete_data[_index] = data['VIX Close']
            elif _index == 'CBOE/VXV':
                self.write_single_to_file(data['CLOSE'], _index[_index.index('/')+1:])
                self.complete_data[_index] = data['CLOSE']
            else:
                self.write_single_to_file(data['Close'], _index[_index.index('/')+1:])
                self.complete_data[_index] = data['Close']

            self.api_call_count += 1

            print (self.complete_data)

            self.check_api_calls()

            # DEV
            #if self.count == 1:
                #break
            #pass
        pass

    def check_api_calls(self):
        """Helps avoid too many Api calls.
        
        """
        if self.api_call_count >= 20:
            time.sleep(600)
            self.api_call_count = 0
        pass

    def write_single_to_file(self, data, name):
        """Writes index data to CSV and Excel files ('./data/[timestr]_[name].csv').
        
        """
        print ('Writing to single file..')
        time_str = time.strftime('%Y%m%d')
        data.to_csv('./data/' + time_str + name + '.csv', index=True)
        print ('Complete!')
        pass

    def write_to_files(self):
        """Writes complete data to CSV and Excel files ('./data').
        
        """
        print ('Writing to files..')
        time_str = time.strftime('%Y%m%d')
        self.complete_data.to_csv('./data/' + time_str + '_fields_daily.csv', index=True)
        #self.complete_data.to_excel('./data/' + time_str + '_fields_daily.xlsx', sheet_name='Fields Daily', index=True)
        print ('Complete!')
        pass

    pass

"""Execute class."""
fields = FieldsDaily()
fields.get_index_data()
fields.write_to_files()