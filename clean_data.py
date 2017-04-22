"""
Ian Doherty
April 22, 2017

This file will hold functions need to clean data sets.

Common data problems:
1. Inconsistent column names
2. Missing data
3. Outliers
4. Duplicate rows
5. Untidy
6. Need to process columns
7. Column types can signal unexpected data values

"""

import pandas as pd

# Get information about a dataFrame
def print_dataframe_info(data):

    # View top and bottom of data set
    data.head()
    data.tail()

    # View the index of column names
    data.columns

    # View number of rows and columns
    data.shape

    # Additional info about dataFrame
    data.info()

    pass
