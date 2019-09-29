# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import datetime
import time
import seaborn as sns
import matplotlib.pyplot as plt

from pandas.plotting import autocorrelation_plot
from pandas import Series
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_acf

# import statsmodels.api as sm
# import statsmodels.formula.api as smf

# from sklearn import svm
# from sklearn import linear_model as lin
# from sklearn.neighbors import KNeighborsRegressor as knn
# from sklearn import tree as dt
# from sklearn.neural_network import MLPRegressor as nnet
# from sklearn.ensemble import GradientBoostingRegressor as gbe

# from sklearn.externals import joblib
# from sklearn.model_selection import cross_val_score, ShuffleSplit
# from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, explained_variance_score

ifile="../sdr-data/traces/traces-03112018-Cen1a4.csv"
df=pd.read_csv(ifile,header=0)

# print df['rssi'].autocorr()
# print df['rssi'].autocorr(lag=10)
# print df['rssi'].autocorr(lag=100)
# print df['rssi'].autocorr(lag=1000)
# print df['rssi'].autocorr(lag=5000)
# print df['rssi'].autocorr(lag=10000)
# print df['rssi'].autocorr(lag=20000)

# print df['rssi'].autocorr(lag=50)


# f, axes = plt.subplots(2, 2, figsize=(6, 7), sharex=False)

# lg = 40
fim=71471
plot_acf(df.loc[:16000,'rssi'],lags=50)
# ax1 = plot_acf(df.loc[:fim,'rssi'],lags=10,title='ACF - lag 10',ax=axes[0,0])
# # ax2 = plot_acf(df.loc[:fim,'rssi'],lags=100,title='ACF - lag 100',ax=axes[0,1])
# ax3 = plot_acf(df.loc[:fim,'rssi'],lags=1000,title='ACF - lag 1000',ax=axes[0,1])
# ax4 = plot_acf(df.loc[:fim,'rssi'],lags=5000,title='ACF - lag 5000',ax=axes[1,0])
# ax5 = plot_acf(df.loc[:fim,'rssi'],lags=10000,title='ACF - lag 10000',ax=axes[1,1])
# ax6 = plot_acf(df.loc[:fim,'rssi'],lags=lg,title='ACF - Latency',ax=axes[2,1])

# autocorrelation_plot(df.loc[:300,'rssi'],lags=50)
# sns.despine(left=True)


# plt.setp(axes, yticks=[])
plt.tight_layout()
# plt.suptitle("Partial Autocorrelation", size=12)
plt.show()