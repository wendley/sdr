# Gera mapa de calor da matrix de correlacao
# https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec

import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import seaborn as sns
import numpy as np
from tkinter import *

# ifile="/home/wendley/MEGA/MegaCloud/Documentos/PhD/Codigos/sdr-data/traces/traces-03112018-Cen1a4.csv"
ifile="../sdr-data/traces/traces-03112018-Cen1a4.csv"
df=pd.read_csv(ifile,header=0)

# Remove coluna 'unnamed'
df.rename({"Unnamed: 0":"a"}, axis="columns", inplace=True)
df.drop(["a"], axis=1, inplace=True)

# Step 0 - Read the dataset, calculate column correlations and make a seaborn heatmap

# df.corr().plot()
# corr = df.corr() # Pearson
# corr = df.corr(method='kendall')
corr = df.corr(method='spearman')
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask,k=1)] = True #k=1 p/ mostrar diagonal
with sns.axes_style("white"):
	# ax = sns.heatmap(corr, mask=mask, vmax=.3, square=True)

	ax = sns.heatmap(
	    corr, 
	    mask=mask,
	    vmin=-1, vmax=1, center=0,
	    cmap=sns.diverging_palette(20, 220, n=200),
	    square=True,
	    annot=True,
	    fmt = '.2f',
	    linewidths=.5
	)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
)

pp = PdfPages('mapa8v-spearman.pdf')
# plt.show()
# plt.figure(figsize=(5,5))
# plt.rcParams["figure.figsize"] = (6,6)
plt.plot()
# plt.tight_layout()
# plt.show()
# plt.title('Pearson Correlation')
plt.title('Spearman Correlation')
pp.savefig(bbox_inches='tight')

d = pp.infodict()
d['Title'] = 'Multipage PDF Example'
d['Author'] = 'Wendley S. Silva'
d['Subject'] = 'Heatmap'
d['Keywords'] = 'PhD, UFMG, Brazil'
d['CreationDate'] = datetime.datetime(2019, 06, 15)
d['ModDate'] = datetime.datetime.today()

pp.close()
# with PdfPages('foo.pdf') as pdf:
# 	pdf.savefig()
# 	plt.close()