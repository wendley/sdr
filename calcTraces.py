# -*- coding: utf-8 -*-
# import numpy as np
import pandas as pd
# import datetime
# import time
#import seaborn as sns
#import matplotlib.pyplot as plt

ifile="../sdr-data/traces.csv"
df=pd.read_csv(ifile,header=0,index_col=0)

aux = df['txentrega'].diff()

aux[0]=0

print(aux[0])

df ['diff-txentrega'] = aux

print(df.head())

ifile2="../sdr-data/traces2.csv"
df.to_csv(ifile2)

# df=pd.read_csv(ifile2,header=0,index_col=0)

print(df.head())