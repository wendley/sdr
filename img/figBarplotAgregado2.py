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

# VIEW: Exemplo [1] @test (1)

# ifile="/home/wendley/MEGA/MegaCloud/Documentos/PhD/Codigos/sdr-data/traces/traces-03112018-Cen1a4.csv"
ifile="../../sdr-data/traces/MultiGraph-Agregado.csv"
df=pd.read_csv(ifile,header=0)


errors=df[['errTxEntrega','errRelacao','errGain-Index']]
errors.rename({"errTxEntrega":"Delivery rate"}, axis="columns", inplace=True)
errors.rename({"errRelacao":"TPRP"}, axis="columns", inplace=True)
errors.rename({"errGain-Index":"Gain-Index"}, axis="columns", inplace=True)
hat = ("/",".")

df.rename({"TxEntrega":"Delivery rate"}, axis="columns", inplace=True)
df.rename({"Relacao":"TPRP"}, axis="columns", inplace=True)

# ax=df[['TxEntrega','Relacao']].plot.bar(yerr=errors, capsize=3, secondary_y= 'Relacao', legend=True, width=0.7, rot= 0)
ax  = df['Delivery rate'].plot(yerr=errors, capsize=3, kind="bar", width=0.3, position=1, legend=True, rot= 0, hatch='\\',colormap='Set1',figsize=(7, 6))
ax2 = df['TPRP'].plot(yerr=errors, capsize=3, secondary_y=True, kind="bar", width=0.3, position=0, legend=True, mark_right=True, rot= 0, hatch='//',colormap='Accent')
# ax2 = ax.twinx()
ax.set_ylabel('Delivery (%)')
ax.set_ylim(50,109)
ax.set_xlim(-0.5,4.5)
ax2.set_ylim(0,4)

ax.tick_params(axis='y',which='minor', color='k')
# ax.set_xticklabels(ax.get_xticklabels())
# ax.right_ax.set_ylabel('Ratio')
ax2.set_ylabel('TPRP')
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

# ax.legend(['Delivery','Ratio (right)'],loc=1,frameon = True,framealpha=1,shadow=True)
# ax2.legend(['Ratio','oooo'],loc=(.75,.90),frameon = False)
# ax.right_ax.legend(loc=(.5,.05), frameon = False)
ax2.set_xticklabels(df['LQE'])
# plt.grid()
plt.title('Delivery - aggregated')
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