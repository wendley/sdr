# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import datetime
import time
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm

from pandas.plotting import autocorrelation_plot
from pandas import Series
from statsmodels.tsa.stattools import adfuller, acf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_acf
from scipy.stats import norm

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

df.rename({"Unnamed: 0":"a"}, axis="columns", inplace=True)
df.drop(["a"], axis=1, inplace=True)
# f, axes = plt.subplots(3, 2, figsize=(6, 8), sharex=False)

lg = 40
fim=5000

for i in df:
	print i
	adf, p_value, usedlag, nobs, critical_values, values = adfuller(df[i])
	print ("ADF is ", adf)
	print ("p value is ", p_value)
	print ("lags used are ", usedlag)
	print ("Number of observations are ", nobs)
	print ("Critical Values are", critical_values)

# plot_acf(df.loc[:50,'prr'])
# ax1 = df.loc[:fim,'rssi'].diff().plot(title='ACF - RSSI')
# ax2 = plot(df.loc[:fim,'snr'],lags=lg,title='ACF - SNR',ax=axes[0,1])
# ax3 = plot(df.loc[:fim,'prr'],lags=lg,title='ACF - PRR',ax=axes[1,0])
# ax4 = plot(df.loc[:fim,'txentrega'],lags=lg,title='ACF - Delivery',ax=axes[1,1])
# ax5 = plot(df.loc[:fim,'relacao'],lags=lg,title='ACF - Ratio',ax=axes[2,0])
# ax6 = plot(df.loc[:fim,'latencia-ms'],lags=lg,title='ACF - Latency',ax=axes[2,1])

# aux = df.loc[:72000,'rssi']
# aux = df.loc[:75000,'rssi']
# autocorrelation_plot(aux)

# aux.plot()
# aux.rolling(window=50).mean().plot()

# ax1 = plot_acf(aux,lags=20, title='ACF - RSSI')
# sns.distplot(aux[1:], hist = False, rug=False, fit=norm, color="r", kde = True, kde_kws = {'linewidth': 2, "shade": True})
# sns.despine(left=True)


# plt.setp(axes, yticks=[])
# plt.tight_layout()
# plt.suptitle("Partial Autocorrelation", size=12)
# plt.show()