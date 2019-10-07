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
df=pd.read_csv(ifile,header=0)

ingles = True

errors=df[['errTxEntrega','errRelacao','errGain-Index']]
errors.rename({"errTxEntrega":"TxEntrega"}, axis="columns", inplace=True)
errors.rename({"errRelacao":"Relacao"}, axis="columns", inplace=True)
errors.rename({"errGain-Index":"Gain-index"}, axis="columns", inplace=True)
hat = ("/",".")

df.rename({"CustoEnerg":"Energy cost"}, axis="columns", inplace=True)


ax  = df['Gain-index'].plot(yerr=errors, capsize=3, kind="bar", width=0.3, position=1, legend=True, rot= 0, hatch='\\',colormap='Paired',figsize=(7, 6))
ax2 = df['Energy cost'].plot(secondary_y=True, kind="bar", width=0.3, position=0, rot= 0, hatch='//', legend=True, mark_right=True, colormap='Dark2')
# ax2 = ax.twinx()
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.95, box.height])

ax.set_ylim(20,95)
ax2.set_ylim(10000,83000)
ax2.set_xlim(-0.5,4.5)


ax.tick_params(axis='y',which='minor', color='k')
ax.yaxis.grid(True, which='minor', linestyle=':',alpha=0.9)
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))


if ingles :
	plt.title('Energy cost - with artificial noise')
	ax.set_ylabel('Gain-index')
	ax2.set_ylabel('Cost')
	ax2.set_xticklabels(df['LQE'])
	# ax.legend(loc='upper left', bbox_to_anchor=(0.01, 0.92), frameon=True)
	# ax2.legend(['Energy cost (right)'],loc='upper left', bbox_to_anchor=(0.01, 0.862), frameon=True)
else:
	plt.title('Custo energético')
	ax.set_ylabel('Índice do Ganho')
	ax2.set_ylabel('Custo') # Pacotes transmitidos por pacotes recebido


plt.show()

# ------- FIM -------------------------------------