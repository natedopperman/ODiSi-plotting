# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:38:03 2024

@author: Nate
"""

from quickParseODiSI import parse_data
import pandas as pd

                
data = parse_data(r'G:/Shared drives/MMV/lab_tests/deck/13Mar2024/data/20240313_2024-03-13_17-55-24_ch4_full.tsv') ### make sure there is a tare
# using the quickParseODiSI function, import all the data from the file
    
time = data['Time']
tare = data['Data']['Tare']
values = data['Data']['Values']
position = data['Location']['Location_Values']
        
# Convert to DataFrames if not already
time = pd.DataFrame(time)
position = pd.DataFrame(position)
values = pd.DataFrame(values)
values = values.fillna(0)
mean_val = values.values.mean()
std = values.values.std(ddof=1)
        
# time.to_pickle(r"pickle/FLT1time.pkl")
# position.to_pickle(r'pickle/FLT1position.pkl')
# values.to_pickle(r'pickle/FLT1values.pkl')

# time.to_pickle(r"pickle/FLB2time.pkl")
# position.to_pickle(r'pickle/FLB2position.pkl')
# values.to_pickle(r'pickle/FLB2values.pkl')
            
# time.to_pickle(r"pickle/FLT2time.pkl")
# position.to_pickle(r'pickle/FLT2position.pkl')
# values.to_pickle(r'pickle/FLT2values.pkl')
            
time.to_pickle(r"pickle/FLB1time.pkl")
position.to_pickle(r'pickle/FLB1position.pkl')
values.to_pickle(r'pickle/FLB1values.pkl')
            