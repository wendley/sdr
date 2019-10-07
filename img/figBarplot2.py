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

# ifile="../../sdr-data/results/result-toGraph-c1.csv"
ifile="../../sdr-data/results/result-toGraph-c2.csv"
df=pd.read_csv(ifile,header=0,index_col=0)


ingles = True

errors=df[['errTxEntrega','errRelacao','errGain-Index']]

errors.rename({"errTxEntrega":"Delivery rate"}, axis="columns", inplace=True)
errors.rename({"errRelacao":"TPRP"}, axis="columns", inplace=True)	
errors.rename({"errGain-Index":"Gain-Index"}, axis="columns", inplace=True)
hat = ("/",".")

df.rename({"TxEntrega":"Delivery rate"}, axis="columns", inplace=True)
df.rename({"Relacao":"TPRP"}, axis="columns", inplace=True)

ax  = df['Delivery rate'].plot(kind="bar", yerr=errors, capsize=3,  width=0.3, position=1, legend=True, rot=0, hatch='\\',colormap='Pastel1',figsize=(7, 6))
ax2 = df['TPRP'].plot(kind="bar", yerr=errors, capsize=3, secondary_y=True, width=0.3, position=0, legend=True, mark_right=True, rot= 0, hatch='//')

# box = ax.get_position()
# ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

ax.set_ylim(50,102)
ax.set_xlim(-0.5,4.5)
ax.tick_params(axis='y',which='minor', color='k')
ax.yaxis.grid(True, which='minor', linestyle=':',alpha=0.9)
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
ax2.set_ylim(0,8)

if ingles :
	plt.title('Delivery rate - with artificial noise')
	ax.set_ylabel('Delivery (%)')
	# ax.legend(['Delivery rate'],loc='upper left', bbox_to_anchor=(0.71, 0.922), frameon=True)
	ax2.set_ylabel('TPRP') # Transmitted Packets per received packets
	# ax2.legend(['TPRP (right)'],loc='upper left', bbox_to_anchor=(0.71, 0.86),frameon=True)
else:
	plt.title('Taxa de entrega')
	ax.set_ylabel('Taxa de entrega (%)')
	ax.legend(['Taxa de entrega'],loc='upper left', bbox_to_anchor=(0.01, 0.862), frameon=True)
	ax2.set_ylabel('TPRP') # Pacotes transmitidos por pacotes recebido
	ax2.legend(['TPRP (direito)'],loc='upper left', bbox_to_anchor=(0.01, 0.8),frameon=True)


plt.show()

# ------- FIM -------------------------------------

# ax2 = ax.twinx()
# plt.title('Delivery')

# print(df['TxEntrega'].max())
# ax.hlines(99.3, -.5,.5, linestyles='dashed')
# ax.annotate('max delivery',(-0.4,99.3))



# ax.set_xticklabels(ax.get_xticklabels())
# ax.right_ax.set_ylabel('Ratio')

# ax.set_xticklabels(
#     ax.get_xticklabels(),
#     rotation=45,
#     horizontalalignment='right'
# )
# plt.legend(loc='upper left')

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