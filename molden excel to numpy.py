# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 00:31:32 2019

@author: XIAN
"""
import pandas as pd
import numpy as np

df = pd.read_excel('/Users/XIAN/Documents/xian fyp/final 4.4 all data - Copy.xlsx')
df = df.values
print(df.shape)

np.save('/Users/XIAN/Documents/xian fyp/Molden 44', df)

