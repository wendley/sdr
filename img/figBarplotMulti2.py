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
ifile="../../sdr-data/traces/MultiGraph.csv"
df=pd.read_csv(ifile,header=0,index_col=0)


errors=df[['errNo12','errNo13','errNo15','errNo16']]
errors.rename({"errNo12":"No12"}, axis="columns", inplace=True)
errors.rename({"errNo13":"No13"}, axis="columns", inplace=True)
errors.rename({"errNo15":"No15"}, axis="columns", inplace=True)
errors.rename({"errNo16":"No16"}, axis="columns", inplace=True)
hat = ("/",".")

# ax=df[['TxEntrega','Relacao']].plot.bar(yerr=errors, capsize=3, secondary_y= 'Relacao', legend=True, width=0.7, rot= 0)
ax  = df['No12'].plot(yerr=errors, capsize=3, kind="bar", width=0.2, position=1.5, legend=True, rot= 0, hatch='\\',colormap='Pastel1',figsize=(7, 6))
ax2 = df['No13'].plot(yerr=errors, capsize=3, kind="bar", width=0.2, position=0.5, legend=True, mark_right=True, rot= 0, hatch='//')
ax3 = df['No15'].plot(yerr=errors, capsize=3, kind="bar", width=0.2, position=-0.5, legend=True, mark_right=True, rot= 0, hatch='-',colormap='Pastel2')
ax4 = df['No16'].plot(yerr=errors, capsize=3, kind="bar", width=0.2, position=-1.5, legend=True, mark_right=True, rot= 0, hatch='.')
# ax2 = ax.twinx()
ax.set_ylabel('Delivery (%)')
ax.set_ylim(50,105)
ax.set_xlim(-0.6,4.6)

ax.tick_params(axis='y',which='minor', color='k')
# ax.set_xticklabels(ax.get_xticklabels())
# ax.right_ax.set_ylabel('Ratio')
# ax2.set_ylabel('Ratio')
ax.yaxis.grid(True, which='minor', linestyle=':',alpha=0.9)
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

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

ax.legend(['Node12','Node13','Node15','Node16'],loc=4,frameon = True,framealpha=1,shadow=True)

# ax2.set_xticklabels(df['LQE'])
# plt.grid()
plt.title('Delivery')
plt.show()
# ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)