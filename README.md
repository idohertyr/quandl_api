# cboe_vix_futures

#### A repo of scripts for pulling data from the Quandl Api.

##### QuandlFuturesVix.py

This python script collects the settle and close price of each
futures contract. Then it appends the contract name and collects the
close price from the VIX Index. The data is then combined in
a pandas DataFrame and exported to CSV and Excel file formats.