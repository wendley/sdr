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

from statsmodels.tsa.stattools import adfuller

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





# result= adfuller(df['rssi'])
# print('ADF Statistic: %f' % result[0])
# print('p-value: %f' % result[1])
# print('Critical Values:')
# for key, value in result[4].items():
# 	print('\t%s: %.3f' % (key, value))

# print df['rssi'].autocorr()
# print df['rssi'].autocorr(lag=10)
# print df['rssi'].autocorr(lag=100)
# print df['rssi'].autocorr(lag=1000)
# print df['rssi'].autocorr(lag=5000)
# print df['rssi'].autocorr(lag=10000)
# print df['rssi'].autocorr(lag=20000)

# print df['rssi'].autocorr(lag=50)


f, axes = plt.subplots(3, 2, figsize=(6, 8), sharex=False)

lg = 40
fim=70000
# plot_acf(df.loc[:50,'prr'])
ax1 = plot_acf(df.loc[:fim,'rssi'],lags=lg,title='ACF - RSSI',ax=axes[0,0])
ax2 = plot_acf(df.loc[:fim,'snr'],lags=lg,title='ACF - SNR',ax=axes[0,1])
ax3 = plot_acf(df.loc[:fim,'prr'],lags=lg,title='ACF - PRR',ax=axes[1,0])
ax4 = plot_acf(df.loc[:fim,'txentrega'],lags=lg,title='ACF - Delivery',ax=axes[1,1])
ax5 = plot_acf(df.loc[:fim,'relacao'],lags=lg,title='ACF - Ratio',ax=axes[2,0])
ax6 = plot_acf(df.loc[:fim,'latencia-ms'],lags=lg,title='ACF - Latency',ax=axes[2,1])

# autocorrelation_plot(df.loc[:17000,'rssi'])
# sns.despine(left=True)


# # plt.setp(axes, yticks=[])
# plt.tight_layout()
# # plt.suptitle("Partial Autocorrelation", size=12)
# plt.show()


class StationarityTests: # http://www.insightsbot.com/blog/1MH61d/augmented-dickey-fuller-test-in-python
    def __init__(self, significance=.05):
        self.SignificanceLevel = significance
        self.pValue = None
        self.isStationary = None

    def ADF_Stationarity_Test(self, timeseries, printResults = True):

        #Dickey-Fuller test:
        adfTest = adfuller(timeseries, autolag='AIC')
        
        self.pValue = adfTest[1]
        
        if (self.pValue<self.SignificanceLevel):
            self.isStationary = True
        else:
            self.isStationary = False
        
        if printResults:
            dfResults = pd.Series(adfTest[0:4], index=['ADF Test Statistic','P-Value','# Lags Used','# Observations Used'])

            #Add Critical Values
            for key,value in adfTest[4].items():
                dfResults['Critical Value (%s)'%key] = value

            print('Augmented Dickey-Fuller Test Results:')
            print(dfResults)


sTest = StationarityTests()
sTest.ADF_Stationarity_Test(df['latencia-ms'], printResults = True)
print("Is the time series stationary? {0}".format(sTest.isStationary))