# Gera pairplot da matrix de correlacao
# https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec

import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns
import numpy as np
from tkinter import *

# ifile="/home/wendley/MEGA/MegaCloud/Documentos/PhD/Codigos/sdr-data/traces/traces-03112018-Cen1a4.csv"
ifile="../sdr-data/traces/MultiCost.csv"
df=pd.read_csv(ifile,header=0)


# # Remove coluna 'unnamed'
# df.rename({"Unnamed: 0":"a"}, axis="columns", inplace=True)
# df.drop(["a"], axis=1, inplace=True)

# Step 0 - Read the dataset, calculate column correlations and make a seaborn heatmap

# df.corr().plot()
# corr = df.corr() # Pearson
# corr = df.corr(method='kendall')

# corr = df.corr(method='spearman')
# mask = np.zeros_like(corr)
# mask[np.triu_indices_from(mask,k=1)] = True #k=1 p/ mostrar diagonal
# with sns.axes_style("white"):
# 	# ax = sns.heatmap(corr, mask=mask, vmax=.3, square=True)
# 	ax = sns.heatmap(
# 	    corr, 
# 	    mask=mask,
# 	    vmin=-1, vmax=1, center=0,
# 	    cmap=sns.diverging_palette(20, 220, n=200),
# 	    square=True,
# 	    annot=True,
# 	    fmt = '.2f',
# 	    linewidths=.5
# 	)

# ax.set_xticklabels(
#     ax.get_xticklabels(),
#     rotation=45,
#     horizontalalignment='right'
# )
# plt.legend(loc='upper left')
# errors=df[['errNo12','errNo14','errNo16']]
# errors.rename({"errNo12":"No12"}, axis="columns", inplace=True)
# errors.rename({"errNo14":"No14"}, axis="columns", inplace=True)
# errors.rename({"errNo16":"No16"}, axis="columns", inplace=True)
hat = ("/",".")

# ax=df[['TxEntrega','Relacao']].plot.bar(yerr=errors, capsize=3, secondary_y= 'Relacao', legend=True, width=0.7, rot= 0)
ax  = df['No12'].plot(kind="bar", width=0.3, position=1.5, legend=True, rot= 0, hatch='\\',colormap='Pastel1')
ax2 = df['No14'].plot(kind="bar", width=0.3, position=0.5, legend=True, mark_right=True, rot= 0, hatch='//')
ax3 = df['No16'].plot(kind="bar", width=0.3, position=-0.5, legend=True, mark_right=True, rot= 0, hatch='.',colormap='Pastel2')
# ax2 = ax.twinx()
ax.set_ylabel('gain index * sends')
ax.set_ylim(10000,46000)
ax.set_xlim(-0.6,4.6)

# ax.tick_params(axis='y',which='minor', color='k')
# ax.set_xticklabels(ax.get_xticklabels())
# ax.right_ax.set_ylabel('Ratio')
# ax2.set_ylabel('Ratio')
ax.yaxis.grid(True, which='major', linestyle=':',alpha=0.9)
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

# bars = ax.patches
# patterns =('/', '+', 'x','-','//','O','o','\\','\\\\')
# hatches = [p for p in patterns for i in range(len(df))]
# for bar, hatch in zip(bars, hatches):
#     bar.set_hatch(hatch)


# bars = ax.right_ax.patches
# patterns =('.', '+', 'x','-','//','O','o','\\','\\\\')
# hatches = [p for p in patterns for i in range(len(df))]
# for bar, hatch in zip(bars, hatches):
#     bar.set_hatch(hatch)

ax.legend(['Node12','Node14','Node16'],loc=2,frameon = True,framealpha=1,shadow=True)
# ax2.legend(['Node14'],loc=(.85,.85),frameon = True)
# ax.right_ax.legend(loc=(.5,.05), frameon = False)
ax2.set_xticklabels(df['LQE'])
# plt.grid()
plt.title('Energy cost')
plt.show()
# ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)

# pp = PdfPages('mapa8v-spearman.pdf')
# plt.plot()
# # plt.tight_layout()
# # plt.show()
# plt.title('Spearman Correlation')
# pp.savefig(bbox_inches='tight')

# d = pp.infodict()
# d['Title'] = 'Multipage PDF Example'
# d['Author'] = 'Wendley S. Silva'
# d['Subject'] = 'Heatmap'
# d['Keywords'] = 'PhD, UFMG, Brazil'
# d['CreationDate'] = datetime.datetime(2019, 06, 15)
# d['ModDate'] = datetime.datetime.today()

# pp.close()
# # with PdfPages('foo.pdf') as pdf:
# # 	pdf.savefig()
# # 	plt.close()