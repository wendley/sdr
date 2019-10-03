# Gera mapa de calor da matrix de correlacao
# https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec

import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import seaborn as sns
import numpy as np
from Tkinter import *

# ifile="/home/wendley/MEGA/MegaCloud/Documentos/PhD/Codigos/sdr-data/traces/traces-03112018-Cen1a4.csv"
ifile="../../sdr-data/traces2.csv"
df=pd.read_csv(ifile,header=0,index_col=0)

# Remove coluna 'unnamed'
# df.rename({"Unnamed: 0":"a"}, axis="columns", inplace=True)
df.rename({"relacao":"ratio"}, axis="columns", inplace=True)
df.rename({"txentrega":"delivery"}, axis="columns", inplace=True)
df.rename({"diff-txentrega":"diff-delivery"}, axis="columns", inplace=True)
df.rename({"latencia-ms":"latency"}, axis="columns", inplace=True)
df.rename({"potencia":"power"}, axis="columns", inplace=True)
# df.drop(["a"], axis=1, inplace=True)
df.drop(["estimation"], axis=1, inplace=True)


# aux = df.diff() # apply diff method to compute corr over non-stationary
# df=aux


f, (ax1,ax2) = plt.subplots(2,1, figsize=(5.5, 12), sharex=False)

corr = df.corr(method='spearman')
corrdiff = df.diff().corr(method='spearman')

# corr = df.corr(method='kendall')
# corr = df.corr(method='spearman')

mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask,k=1)] = True #k=1 p/ mostrar diagonal
with sns.axes_style("white"):
	# ax = sns.heatmap(corr, mask=mask, vmax=.3, square=True)

	sns.heatmap(
	    corr, 
	    mask=mask,
	    vmin=-1, vmax=1, center=0,
	    cmap=sns.diverging_palette(50, 130, n=200),
	    square=True,
	    annot=True,
	    fmt = '.2f',
	    linewidths=.5,
	    ax=ax1
	)

ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, horizontalalignment='right')

with sns.axes_style("white"):
	# ax = sns.heatmap(corr, mask=mask, vmax=.3, square=True)

	sns.heatmap(
	    corrdiff, 
	    mask=mask,
	    vmin=-1, vmax=1, center=0,
	    cmap=sns.diverging_palette(50, 130, n=200),
	    square=True,
	    annot=True,
	    fmt = '.2f',
	    linewidths=.5,
	    ax=ax2
	)
	
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, horizontalalignment='right')

ax1.set_title('Spearman correlation',size=11)
ax2.set_title('Spearman correlation from First Order Difference',size=11)

# pp = PdfPages('mapa8v-spearman.pdf')
# plt.show()
plt.plot()
# plt.title('Spearman Correlation')
plt.tight_layout()
plt.show()


# pp.savefig(bbox_inches='tight')

# d = pp.infodict()
# d['Title'] = 'Multipage PDF Example'
# d['Author'] = 'Wendley S. Silva'
# d['Subject'] = 'Heatmap'
# d['Keywords'] = 'PhD, UFMG, Brazil'
# d['CreationDate'] = datetime.datetime(2019, 06, 15)
# d['ModDate'] = datetime.datetime.today()

# pp.close()