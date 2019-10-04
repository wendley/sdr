# -*- coding: utf-8 -*-
# import numpy as np
import pandas as pd
# import datetime
# import time
#import seaborn as sns
#import matplotlib.pyplot as plt


# ifile1="../sdr-data/traces2.csv"
# df1=pd.read_csv(ifile1,header=0,index_col=0)


# ifile2="../sdr-data/traces3.csv"
# df2=pd.read_csv(ifile2,header=0,index_col=0)

# aux = df2['txentrega'].diff()

# aux[0]=0

# df2['diff-txentrega'] = aux

# # print(df.head())


# ifile4="../sdr-data/traces4.csv"
# df2.to_csv(ifile4)

# frames = [df1,df2]

# ifile5="../sdr-data/traces-comb.csv"
# combined_csv = pd.concat(frames)
# combined_csv.to_csv(ifile5)

count = 0

ifile1="../sdr-data/traces5.csv"
df=pd.read_csv(ifile1,header=0,index_col=0)

df = df.drop(df[df.prr > 1].index)
df = df.drop(df[df.prr2 > 1].index)
df = df.drop(df[df.txentrega > 100].index)
df = df.drop(df[df.relacao > 1000].index)
df = df.drop(df[df['latencia-ms'] > 10000].index)

df.to_csv(ifile1)