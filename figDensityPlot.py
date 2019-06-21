# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import datetime
import time
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm

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


f, axes = plt.subplots(3, 2, figsize=(7, 9), sharex=False)
sns.despine(left=True)
# sns.set_palette("pastel")


# df.plot.hist(alpha=0.5, bins=15, grid=True)

# sns.set()


# sns.distplot(df['rssi'], hist = False, kde = True,kde_kws = {'linewidth': 3, "shade": True})
rg = True # rug

ax1=sns.distplot(df['rssi'], hist = False, fit=norm, rug=rg, color="b", kde = True, kde_kws = {'linewidth': 3, "shade": True},ax=axes[0, 0])
(mu, sigma) = stats.norm.fit(df['rssi'])
# print "mu={0}, sigma={1}".format(mu, sigma)
# CROSS CHECK - 
# https://stackoverflow.com/questions/31413934/howto-get-fit-parameters-from-seaborn-distplot-fit
# x_dummy = np.linspace(stats.norm.ppf(0.01), stats.norm.ppf(0.99), 100)
# ax2.plot(x_dummy, stats.norm.pdf(x_dummy, mu, sigma),color="r")
ax1.legend(["normal dist. fit ($\mu=${0:.2g}, $\sigma=${1:.2f})".format(mu, sigma)],frameon=False, prop={'size': 6},loc=1)

ax2=sns.distplot(df['snr'], hist = False, fit=norm, rug=rg, color="r", kde = True, kde_kws = {'linewidth': 3, "shade": True},ax=axes[0, 1])
(mu, sigma) = stats.norm.fit(df['snr'])
ax2.legend(["normal dist. fit ($\mu=${0:.2g}, $\sigma=${1:.2f})".format(mu, sigma)],frameon=False, prop={'size': 6},loc=1)

ax3=sns.distplot(df['prr'], hist = False, fit=norm, rug=rg, color="g", kde = True, kde_kws = {'linewidth': 3, "shade": True},ax=axes[1, 0])
(mu, sigma) = stats.norm.fit(df['prr'])
ax3.legend(["normal dist. fit ($\mu=${0:.2g}, $\sigma=${1:.2f})".format(mu, sigma)],frameon=False, prop={'size': 6}, loc=1)

# ax4=sns.distplot(df['prr2'], hist = False, color="m", kde = True,kde_kws = {'linewidth': 3, "shade": True},ax=axes[1, 0])
# ax3.legend(['prr','prr2'],loc=1)
# ax4.set_xticklabels='lqe'
ax4=sns.distplot(df['txentrega'], hist = False, fit=norm, rug=rg, color="c", kde = True, kde_kws = {'linewidth': 3, "shade": True},ax=axes[1, 1])
ax4.set_xlabel('delivery')
(mu, sigma) = stats.norm.fit(df['txentrega'])
ax4.legend(["normal dist. fit ($\mu=${0:.2g}, $\sigma=${1:.2f})".format(mu, sigma)],frameon=False, prop={'size': 6}, loc=1)

ax5=sns.distplot(df.loc[:53000,'relacao'], hist = False, fit=norm, rug=rg, color="y", kde = True,kde_kws = {'linewidth': 3, "shade": True},ax=axes[2, 0])
ax5.set_xlabel('ratio')
(mu, sigma) = stats.norm.fit(df.loc[:53000,'relacao'])
ax5.legend(["normal dist. fit ($\mu=${0:.2g}, $\sigma=${1:.2f})".format(mu, sigma)],frameon=False, prop={'size': 6}, loc=1)

ax6=sns.distplot(df.loc[:35000,'latencia-ms'], hist = False, fit=norm, rug=rg, color="m", kde = True,kde_kws = {'linewidth': 3, "shade": True},ax=axes[2,1]) 
ax6.set_xlabel('latency')
(mu, sigma) = stats.norm.fit(df.loc[:35000,'latencia-ms'])
ax6.legend(["normal dist. fit ($\mu=${0:.2g}, $\sigma=${1:.2f})".format(mu, sigma)],frameon=False, prop={'size': 6}, loc=2)

# (mu, sigma) = stats.norm.fit(df['rssi'])
# print "mu={0}, sigma={1}".format(mu, sigma)


# plt.setp(axes, yticks=[])
plt.tight_layout()
plt.suptitle("Kernel Density Estimation", size=12, y=.999,verticalalignment='top')
plt.show()