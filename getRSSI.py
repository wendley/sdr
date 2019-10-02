#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 <Wendley S. Silva (http://github.com/wendley)>.
# Jul/2018
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
#
# This module get the RSSI value, PRR and calculate the LQE and update
# the USRP gain  (Tx). More details in https://bitbucket.org/wendley/gr-lqe


import numpy, pmt, time, datetime
import pandas as pd
import os
import math
from numpy import convolve
from gnuradio import gr
from gnuradio import uhd
#from sklearn import svm # Support Vector Machine
from sklearn import tree as dt # DecisionTreeRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn import linear_model # Para LQL
from sklearn.externals import joblib
from pyadwin import Adwin


class getRSSI(gr.sync_block):
	"""
	Estimates the Link Quality using RSSI, PRR or PRR2.
	[1] https://github.com/osh/gr-uhdgps
	[2] https://github.com/osh/gr-eventstream
	"""

	def __init__(self, printPower=False, method=1, filters=1, window=40, minRSSI=-100, maxRSSI=-56, timeout=0.7, alphaHW=0.2, betaHW=0.1, gammaHW=0.05):
		gr.sync_block.__init__(self,
							   name="LQE",
							   in_sig=[],
							   out_sig=[])

		self.printPower = printPower
		self.method = method
		self.window = window
		self.minRSSI = minRSSI
		self.maxRSSI = maxRSSI
		self.alphaHW = alphaHW
		self.betaHW = betaHW
		self.gammaHW = gammaHW
		self.filter = filters
		self.timeoutML = timeout

		self.serie=[]
		self.seriePRR=[]
		self.serieACK=[]
		self.serieLACK=[] # Long range window
		self.seriePCK=[]
		self.serieLPCK=[] # Long range
		self.serieML=[] # For Machine Learning fit
		self.serieLQL=[] # For 4C - Foresee
		self.serieSNR=[]
		self.estimSVMR = 0.0
		self.estimSVMRLQL = 0.0
		self.tempML = []
		self.tempLQL = []
		self.serieTarget=[] # For ML fit
		self.serieTargetLQL=[] # For Foresee
		self.finalSerieML = []
		self.finalSerieLQL = []
		self.serieErroLQM3 = []
		self.serieErroSVMRLQL = []
		self.ackCount = 0
		self.sendedPacks = 0
		self.kRssi = 0.0
		self.Rssi = 0
		self.snr = 0.0
		self.emaRssi = 0
		self.geralPRR = 0  # Short range
		self.geralLPRR = 0 # Long range
		self.geralPRR2 = 0
		self.geralPRR2modif = 0
		self.geralSends = 1 # Total number of sends
		self.geralSendOrder = 0 # Total number of send orders
		self.mediaSNR = 0.0
		self.startT = 0 # start time for ML
		self.split = 0 # split time for ML
		self.outPck = 0 # start time for packet time
		self.intAck = 0 # end time for packet time
		self.diffTempo = 0.0
		#self.ETX = 0.0 # ETX (1 to 6, because 6 is the max resends)
		self.estimETX = 0.0 # ETX (0 to 1)
		self.profund = []
		self.folhas = []
		self.serieTempoTotalAck = []
		self.serieTempoML = []

		self.serieTreinoRssi = []
		self.serieTreinoPRR = []
		self.serieTreinoPRR2 = []
		self.serieTreinoSNR = []
		self.serieTreinoTxEntrega = []
		self.serieTreinoRelacao = []
		self.matrix = [] # Para treinamento ML
		self.treinaML = True # True para treinamento (coleta de dados / traces. Usar estimador PRR2)
		self.treinado = False
		self.forcaLQE = 0.5 # Valor forçado para estimativa (usado na coleta dos dados)

		#self.contaReducao = 0 # Conta a qtde vezes que a serie para LQR3 foi reduzida
		self.cont999 = 1 # contagem para evitar duas impressoes das estatisticas
		self.contaConceptDrift = 0
		self.treinar = True
		self.contaTreinos = 0

		self.fnRSSI="/home/wendley/Experimentos/SerieRSSI.txt"
		self.fnRSSIKalman="/home/wendley/Experimentos/SerieRSSIKalman.txt"
		self.fnPRR="/home/wendley/Experimentos/SeriePRR.txt"
		self.fnPRRRssi="/home/wendley/Experimentos/SeriePRRRssi.txt"
		self.fnPRR2levels="/home/wendley/Experimentos/SeriePRR2levels.txt"
		self.fnPRR2="/home/wendley/Experimentos/SeriePRR2.txt"
		self.timestr = ""

		self.message_port_register_in(pmt.intern("RSSIin"))
		self.message_port_register_in(pmt.intern("Ackin"))
		self.message_port_register_in(pmt.intern("SNR"))
		self.message_port_register_in(pmt.intern("sendPacks"))
		self.message_port_register_in(pmt.intern("sendOrder"))
		self.message_port_register_in(pmt.intern("lostPacks"))
		self.message_port_register_out(pmt.intern("estimation"))

		self.set_msg_handler(pmt.intern("RSSIin"), self.handler)
		self.set_msg_handler(pmt.intern("Ackin"), self.handlerAck)
		self.set_msg_handler(pmt.intern("SNR"), self.handlerSNR)
		self.set_msg_handler(pmt.intern("lostPacks"), self.handlerPack)
		self.set_msg_handler(pmt.intern("sendPacks"), self.handlerSendPack)
		self.set_msg_handler(pmt.intern("sendOrder"), self.handlerSendOrder)

		# self.clf = svm.SVR()
		self.clf = dt.DecisionTreeRegressor()# max_depth=8) # LQM3
		self.reg = linear_model.BayesianRidge() # LQL

		self.clf = joblib.load('fileTrain.joblib')
		self.reg = joblib.load('fileTrainLQL.joblib')

		self.profund.append(self.clf.tree_.max_depth)

		self.startT = time.time()
		self.adwin = Adwin(0.01) # Padrao

	def work(self, input_items, output_items):
		assert (False)


	def handler(self, pdu): # Acionado sempre que chega um valor de RSSI
		self.Rssi = pmt.to_python(pdu)

		if self.printPower: print "Potencia do meio: %6.2f dB" % (self.Rssi)

		if self.filter == 3: # Kalman
			if len(self.serie) < self.window*4:
				self.serie.append(self.Rssi)
			else:
				self.serie.append(self.Rssi)
				del(self.serie[0])

			if len(self.serie) > 10:
				self.kRssi = self.kalmanFilter(self.serie)
				# print "\n DEBUG ------- RSSI with Kalman filter: %6.2f ----- \n"  % (self.kRssi)
				# print type (self.kRssi)

		else:
			# Cria janela móvel limitada (para não extrapolar a memória) para cálculo das médias
			self.serie.append(self.Rssi)
			if len(self.serie) > self.window*4:
				del(self.serie[0])

			if len(self.serie)>2*self.window/2: # limitação da EMA
				self.emaRssi = self.ema(self.serie, self.window/2)
			# print "\n DEBUG ------- RSSI with EWMA filter: %6.2f ----- \n"  % (self.emaRssi)


	def handlerAck(self, pdu):
		tipo = pmt.to_python(pdu)

		if tipo == 1: # Sinaliza recebimento de um ack
			self.ackCount += 1
			# print "\n--------- \nTotal geral de acks recebidos: %d \n--------- \n" % (self.ackCount)
			self.sendedPacks += 1

			if self.outPck == 0:
				self.outPck = datetime.datetime.now() # muda o tipo de integer para datetime
			self.intAck = datetime.datetime.now()
			self.diffTempo = self.intAck - self.outPck
			# print "\n ----- \nTempo p receber ack: "
			# print (self.diffTempo)
			# print "\n"

			self.serieTempoTotalAck.append(self.diffTempo.microseconds/1000.0) # adiciona os milisegundos do tempo de recebimento de acks

			self.calcPRR(1)
			self.calcLQE()
		elif tipo == 999: # Sinaliza final de arquivo ou de msg, após esvaziar buffer do MAC
			if self.cont999 == 1:
				self.cont999 = 2
			elif self.cont999 == 2: #faz com que somente no segundo 999 (do buffer) eh que haja a chamada do stat
				self.statSummary()


	def handlerSNR(self, pdu): # Acionado sempre que uma leitura de SNR é calculada
		self.snr = pmt.to_python(pdu)

		# Cria janela móvel limitada para cálculo da média do SNR
		if numpy.isnan(self.snr) == False : # só processa se o valor não for NaN
			self.serieSNR.append(self.snr)
			if len(self.serieSNR) > 20 :
				del(self.serieSNR[0])
			self.mediaSNR=self.sma(self.serieSNR,20)
		# print self.mediaSNR


	def handlerPack(self, pdu): # Acionado sempre que ocorre um aviso (gerado pela camada MAC) de pacote perdido
		self.sendedPacks += 1
		self.calcPRR(2)
		self.calcLQE()

	def handlerSendPack(self, pdu): # Acionado sempre que um pacote é de fato enviado (incluindo reenvios)
		self.geralSends += 1
		self.outPck = datetime.datetime.now()
		self.calcLQE()

		# Salva arquivos para scatterplot
		arq1 = open(self.fnRSSI, "a")
		arq1.write(str(self.emaRssi)+'\n') # era self.estimRssi

		arq2 = open(self.fnRSSIKalman, "a")
		arq2.write(str(self.estimRssiKalman)+'\n')

		arq3 = open(self.fnPRR, "a")
		arq3.write(str(self.estimPRR)+'\n')

		arq4 = open(self.fnPRRRssi, "a")
		arq4.write(str(self.estimPRR_Rssi)+'\n')

		arq5 = open(self.fnPRR2levels, "a")
		arq5.write(str(self.estimPRR2levels)+'\n')

		arq6 = open(self.fnPRR2, "a")
		arq6.write(str(self.estimPRR2)+'\n')


		#####################################################
		# #												  # #
		# #												  # #
		# #	 PARA COLETA DE DADOS PARA ESCOLHA DO ML      # #
		# #												  # #
		# #												  # #
		#####################################################

		# Coletar: rssi, prr, snr, prr2, tx entrega, latencia, potencia, variacao tx entrega, variacao prr

		if self.treinaML == True : # setado na linha 118
			if self.ackCount > 0:
				calcTxE = (float(self.ackCount)/self.geralSendOrder)*100.0
				calcRel = self.geralSends/(self.ackCount*1.0) # to force float
			else:
				calcTxE = 0.0
				calcRel = 0.0

			linha=[]
			potencia = 44.0*(1-self.forcaLQE)+45 # calculo igual ao usado no powerControl

			linha.append(self.emaRssi[0])
			linha.append(self.estimPRR)
			linha.append(self.estimPRR2)
			linha.append(float(self.mediaSNR))
			linha.append(calcTxE) # Taxa de entrega
			linha.append(calcRel) # Relacao
			if self.diffTempo == 0.0 or self.diffTempo == 999:
				linha.append(self.diffTempo)
			else:
				linha.append(self.diffTempo.microseconds/1000.0) # miliseconds
			self.diffTempo = 999 #para evitar leituras de tempo repetidas
			linha.append(potencia)
			linha.append(self.forcaLQE)

			self.matrix.append(linha)

			self.method = 4 # força usar PRR2 (para conseguir calcular PRR2). setar valor manualmente na linha 556

		# Fim_if da COLETA



	def handlerSendOrder(self, pdu): # Acionado sempre que uma ordem de transmissão é enviada
		self.geralSendOrder += 1



	def calcPRR(self, type):

		# Cria janela móvel limitada (para não extrapolar a memória) para cálculo das médias

		if self.method == 4 or self.method == 5 or self.method == 7 or self.method == 8: # PRR 2 levels (short and long range)

			if type == 1: # Acionado por um ack recebido (handlerAck)
				self.serieACK.append(1)
				self.seriePCK.append(1)
				self.serieLACK.append(1)
				self.serieLPCK.append(1)

				if len(self.serieACK) >= self.window*2: # short range window
					del(self.serieACK[0])
					if len(self.seriePCK) >= self.window*2:
						del(self.seriePCK[0])

				if len(self.serieLACK) >= self.window*4: # long range window
					del(self.serieLACK[0])
					if len(self.serieLPCK) >= self.window*4:
						del(self.serieLPCK[0])

			elif type == 2: # Acionado por um pacote perdido (handlerPack)
				self.serieACK.append(0)
				self.seriePCK.append(1)
				self.serieLACK.append(0)
				self.serieLPCK.append(1)

				if len(self.seriePCK) >= self.window*2: # short range window
					del(self.seriePCK[0])
					if len(self.serieACK) >= self.window*2:
						del(self.serieACK[0])

				if len(self.serieLPCK) >= self.window*4: # long range window
					del(self.serieLPCK[0])
					if len(self.serieLACK) >= self.window*4:
						del(self.serieLACK[0])



		else: # PRR 1 levels (short range)

			if type == 1: # Acionado por um ack recebido (handlerAck)
				self.serieACK.append(1)
				self.seriePCK.append(1)

				if len(self.serieACK) >= self.window*2:
					del(self.serieACK[0])
					if len(self.seriePCK) >= self.window*2:
						del(self.seriePCK[0])

			elif type == 2: # Acionado por um pacote perdido (handlerPack)
				self.serieACK.append(0)
				self.seriePCK.append(1)

				if len(self.seriePCK) >= self.window*2:
					del(self.seriePCK[0])
					if len(self.serieACK) >= self.window*2:
						del(self.serieACK[0])


		# FILTERS:

		if self.filter == 1:
			# No filter in use
			self.geralPRR = sum(self.serieACK)/float(sum(self.seriePCK)) # PRR from short range

			if self.method == 4 or self.method == 5 or self.method == 7 or self.method == 8: # PRR 2 levels
				self.geralLPRR = sum(self.serieLACK)/float(sum(self.serieLPCK)) # PRR from long range
				# print "\n--------- \nLONG PRR: %2.4f\n---------\n" % (float(self.geralLPRR))
				# print "\n--------- \nLONG PRR LENGTH: %2.4f\n---------\n" % (float(len(self.serieLACK)))


		elif self.filter == 2:
			# Exponential Moving Average filter
			self.geralPRR = self.preEMA(self.serieACK,self.seriePCK, self.window/2)  # PRR from short range

			if self.method == 4 or self.method == 5 or self.method == 7 or self.method == 8: # PRR 2 levels
				self.geralLPRR = self.preEMA(self.serieLACK, self.serieLPCK, self.window*4) # PRR from long range
				# print "\n--------- \nLONG PRR: %2.4f\n---------\n" % (float(self.geralLPRR))
				# print "\n--------- \nLONG PRR LENGTH: %2.4f\n---------\n" % (float(len(self.serieLACK)))


		elif self.filter == 3:
			# Kalman filter
			# self.geralPRR = self.preEMA(self.serieACK,self.seriePCK, self.window/2)
			# self.seriePRR.append(self.preEMA(self.serieACK,self.seriePCK, self.window/2))
			# self.geralPRR = self.kalmanFilter(self.seriePRR)
			# if len(self.serieACK) < n_iter and len(self.seriePCK) < n_iter: # limitação do filtro
			# 	return self.preEMA(self.serieACK, self.seriePCK, self.window/2)
			# else:

			# print "\n--- WARNING: Kalman filter only for RSSI. Using EMA --- \n"

			self.geralPRR = self.preEMA(self.serieACK,self.seriePCK, self.window/2)  # PRR from short range

			if self.method == 4 or self.method == 5 or self.method == 7 or self.method == 8 : # PRR 2 levels
				self.geralLPRR = self.preEMA(self.serieLACK, self.serieLPCK, self.window*4) # PRR from long range
				print "\n--------- \nLONG PRR: %2.4f\n---------\n" % (float(self.geralLPRR))
				# print "\n--------- \nLONG PRR LENGTH: %2.4f\n---------\n" % (float(len(self.serieLACK)))



		elif self.filter == 4:
			# Savitzky-Golay filter
			print "No filter in use"

		elif self.filter == 5:
			# Dynamic mode filter
			print "No filter in use"


		print "\n--------- \nPRR: %2.4f\n---------\n" % (float(self.geralPRR))
		# print "\n--------- \nPRR LENGTH: %2.4f\n---------\n" % (float(len(self.serieACK)))
		# print "\n -------- \n Total de envios: %d \n ----------\n" % self.geralSends


	def preEMA(self, serieA, serieP, window): #Pre-processamento para Exponential Moving Average


		if len(serieA)>2*window and len(serieP)>2*window: # limitação da EMA
			emaSA = self.ema(serieA,window) # Média móvel série Ack
			emaSP = self.ema(serieP,window) # Média móvel série pacotes enviados

		else:
			# Usa SMA enquanto serie esta com poucos dados
			emaSA = self.sma(serieA,len(serieA)) # Média móvel série Ack
			emaSP = self.sma(serieP,len(serieP)) # Média móvel série pacotes enviados

		return emaSA/float(emaSP)  # PRR - Packet Reception Ratio

		serieA=[]
		serieP=[]


	def calcLQE(self): # Calcula LQE e envia a estimativa

		#Range do RSSI
		minRSSI = self.minRSSI
		maxRSSI = self.maxRSSI

		rangeRSSI = maxRSSI - minRSSI

		tempRssi = self.emaRssi

		# print "RSSI suavizado: "
		# print tempRssi

		if tempRssi < minRSSI :
			tempRssi = minRSSI
		elif tempRssi > maxRSSI :
			tempRssi = maxRSSI

		tempKalmanRssi= self.kRssi

		if tempKalmanRssi < minRSSI :
			tempKalmanRssi = minRSSI
		elif tempKalmanRssi > maxRSSI :
			tempKalmanRssi = maxRSSI

		# print "RSSI suavizado: "
		# print tempKalmanRssi

		self.estimRssi = float(1-(tempRssi-minRSSI)/rangeRSSI)

		# print "RSSI Estim: "
		# print self.estimRssi

		self.estimRssiKalman = float(1-(tempKalmanRssi-minRSSI)/rangeRSSI)

		# print "RSSI Estim Kalman: "
		# print self.estimRssiKalman

		# RSSI Instantaneo + Kalman kRssi
		# See calibration in datasheet of AD9361 (Analog Device of B210):
		# http://www.analog.com/media/en/technical-documentation/user-guides/AD9361_Reference_Manual_UG-570.pdf
		# https://www.analog.com/media/en/technical-documentation/data-sheets/AD9361.pdf

		self.estimPRR = float(self.geralPRR)
		self.estimPRR_Rssi = float(min(self.geralPRR, self.estimRssi)) # PRR + RSSI

		self.estimPRR2levels = float(min(self.geralPRR,self.geralLPRR)) # PRR with 2 levels without RSSI
		self.estimPRR2 = float(min(self.geralPRR,self.geralLPRR, self.estimRssi)) # PRR2 Full
		# print "# DEBUG---------- IMPRIMINDO SERIE-ESTIM-PRR2 desmembrada -----------"
		# print(self.geralPRR)
		# print(self.geralLPRR)
		# print(self.estimRssi)




		if self.method == 1:
			#####################################################
			# No estimator - constant gain - maximum gain
			#####################################################

			print "No estimator in use - the tx gain is constant"
			aux1 = 0.0 # Poor quality, maximum gain
			self.message_port_pub(pmt.intern("estimation"),pmt.from_double(aux1))

		elif self.method == 2:
			#####################################################
			# Estimator using ONLY RSSI:
			#####################################################

			if self.filter == 2: #EMA
				self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimRssi))
				# print " DEBUG ---------- RSSI EMA  -----------"
				# print(self.estimRssi)

			elif self.filter == 3: #Kalman
				self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimRssiKalman))

				# print " DEBUG ---------- RSSI KALMAN -----------"
				# print(self.estimRssiKalman)

			print "RSSI method in use"
			# aux = float(self.emaRssi)
			# print "RSSI ------------ %2.4f\n" % (float(aux))
			# self.message_port_pub(pmt.intern("estimation"), pmt.from_double(self.gainTx))

		elif self.method == 3:
			#####################################################
			# Estimator using ONLY traditional PRR:
			#####################################################

			if self.filter == 3: #Kalman
				print "\n--- WARNING: Kalman filter only for RSSI. Using EMA --- \n"

			#print "PRR method in use"

			self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimPRR))

		elif self.method == 4:
			#####################################################
			# PRR 2 levels + RSSI (FULL)
			#####################################################

			#print "Proposed mode in use - under development - the tx gain is constant"
			#This sets the gain
			#gTx=float(self.gainTx)
			if self.treinaML == True : # setado na linha 118
				self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.forcaLQE)) #seta o valor
			else:
				self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimPRR2))

		elif self.method == 5:
			#####################################################
			# NOTE: ETX -  Expected Transmission Count (ETX) --- Previously: PRR 2 levels without RSSI
			# COUTO, D. S. J. D., AGUAYO, D., BICKET, J., AND MORRIS, R. 2003. A high-throughput path metric for multihop
			# wireless routing. In Proceedings of the 9th Annual International Conference on Mobile Computing and
			# Networking (MobiCom ’03). ACM, 134–146.
			# https://pdos.lcs.mit.edu/papers/grid:decouto-phd/thesis.pdf
			# https://en.wikipedia.org/wiki/Expected_transmission_count
			#####################################################

			#self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimPRR2levels)) # Previously: PRR 2 levels without RSSI
			if self.ackCount > 0:
				self.ETX = float(self.geralSends)/self.ackCount
			else:
				self.ETX = 6
			estimETX = (self.ETX - 6)/(-5.0) # Convertion to 0 --- 1 range
			print "ETX raw value ----- : %6.2f" % (self.ETX)
			print "ETX estimation ----- : %6.2f" % (estimETX)
			self.message_port_pub(pmt.intern("estimation"),pmt.from_double(estimETX))




		elif self.method == 6:
			#####################################################
			# Traditional PRR + RSSI
			#####################################################
			self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimPRR_Rssi))


		elif self.method == 7:
			#####################################################
			# LQL - Link Quality Learning --- era Foresee 4C (like)
			# [REF:] Di Caro, Gianni A., et al. "Online supervised incremental learning of link quality estimates
			# in wireless networks." Ad Hoc Networking Workshop (MED-HOC-NET), 2013 12th Annual Mediterranean. IEEE, 2013.
			# - NÃO RETREINA
			#####################################################

			maxValue = 40 # MAX value to serie to training

			if len(self.serieLQL) >= maxValue: # Arbitrary MAX value to training
				del(self.serieLQL[0])
				del(self.serieTargetLQL[0])


			if (self.geralSends%20==0 and self.geralSends>=20) :
				if (self.geralSends%10==0 and len(self.serieLQL)<=maxValue): # So habilita para treinar e retreinar a cada 10 entradas e ate o MaxValue
					self.treinar = True	
				else:
					self.treinar = False

			self.tempLQL.append(self.estimPRR)
			self.tempLQL.append(self.estimRssi)
			self.tempLQL.append(self.mediaSNR)
			self.serieLQL.append(list(self.tempLQL))
			self.tempLQL=[]
			self.serieTargetLQL.append(self.estimPRR) # Target
			self.finalSerieLQL = numpy.array(self.serieLQL)

			if len(self.serieLQL) >= 20: # Somente usado para treinar a primeira vez
				self.finalSerieLQL=numpy.array(self.serieLQL)

				if self.treinar == True :
					self.contaTreinos +=1
					self.reg.fit(self.serieLQL[:-1],self.serieTargetLQL[:-1]) # Treina com todos os dados da serie, exceto o último
				self.finalSerieLQL = self.serieLQL[-1]
				self.finalSerieLQL = numpy.arange(3).reshape(1,-1) # Para duas entradas, usar 	self.finalSerieML = numpy.arange(2).reshape(1,-1)
				self.estimSVMRLQL = float(self.reg.predict(self.finalSerieLQL)) # Predizer somente o ultimo valor da serie
				erroSVMRLQL = numpy.abs(self.estimSVMRLQL - self.serieTargetLQL[-1])
				self.serieErroSVMRLQL.append(erroSVMRLQL)

				# self.timestr = time.strftime("%Y%m%d-%H%M%S") # Se quiser salvar o arquivo de treinamento .joblib
				# filename = "fileTrainLQL"+self.timestr+".joblib"
				filename = "fileTrainLQL2.joblib"
				joblib.dump(self.reg,filename)

			# self.finalSerieLQL = self.serieLQL[-1] # Descomentar essas 3 linhas se o grande if anterior estiver comentado
			# self.finalSerieLQL = numpy.arange(3).reshape(1,-1) # Para duas entradas, usar 	self.finalSerieML = numpy.arange(2).reshape(1,-1)
			# self.estimSVMRLQL = float(self.reg.predict(self.finalSerieLQL))
			self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimSVMRLQL))


		elif self.method == 8:

			###########################################################
			# #													    # #
			# #													    # #
			# # NOTE: PROPOSTA - Machine Learning - LQM3	        # #
			# # Link Quality Estimator using M.L. with triple input # #
			# # NOTE: Usar .format								    # #
			# #													    # #
			###########################################################

			self.split = time.time()
			elapsed = self.split - self.startT


			# TIME CONTROL : RECURSO DE REDUÇÃO TEMPORAL DA SERIE - Usado opcionalmente
			timeControl = True #True para ativar ou False para desativar
			#
			# if timeControl :
			# 	if elapsed > self.timeoutML: # se decorridos mais de xx segundo, a serie eh reduzida pela metade, apagando as entradas mais antigas
			# 		self.serieML = self.serieML[-(len(self.serieML)/2):]
			# 		self.serieTarget = self.serieTarget[-(len(self.serieTarget)/2):]
			# 		self.contaReducao += 1
			#

			if len(self.serieML)>=20 :
				if (self.geralSends%20==0 and self.geralSends<=40): # So habilita para treinar e retreinar a cada 20 entradas e ate o tam max 40
					# self.treinar = True								  # e depois so retreina se houver detecção de concept drift
					pass
				else:
					self.treinar = False

				if len(self.serieML) >= 41: # Arbitrary MAX value to training
					del(self.serieML[0]) # Apaga a entrada mais antiga
					del(self.serieTarget[0]) # Apaga a entrada mais antiga
			else:
				self.treinar = False

			
			# NOTE: CONCEPT DRIFT - Se detectar, retreina a ML

			concDrift = True # False se quiser desativar Conc. Drift
			if concDrift == True :
				if (self.adwin.update(self.emaRssi)): 
					self.treinar = True
					self.contaConceptDrift += 1


			# if len(self.serieML)>=10 : # Usado apenas para treinamento inicial (depois faz o load .joblib e retreina quando detecta concept drift)
			# 	if (self.geralSends%30==0): # So habilita para treinar e retreinar a cada 30 entradas
			# 		self.treinar = True
			# 	else:
			# 		self.treinar = False

			self.tempML.append(self.estimPRR)
			self.tempML.append(self.estimRssi)
			self.tempML.append(self.mediaSNR)
			self.serieML.append(list(self.tempML))
			self.tempML=[]
			self.serieTarget.append(self.estimPRR2) # Target
			self.finalSerieML = numpy.array(self.serieML)

			if len(self.serieML) >= 20:
				self.finalSerieML=numpy.array(self.serieML)
				

				if self.treinar == True : 		# TODO: Liberado para treinar o LQM3
					self.contaTreinos +=1
					tempo1 = datetime.datetime.now()
					self.clf.fit(self.serieML[:-1],self.serieTarget[:-1]) # Treina com todos os dados da serie, exceto o último
					self.treinado = True # para identificar que já houve 1 treinamento
					# self.profund = self.clf.get_depth() # Python3
					self.profund.append(self.clf.tree_.max_depth)
					# self.folhas = self.clf.get_n_leaves() #P ython3
					folhas = numpy.sum(numpy.logical_and(self.clf.tree_.children_left == -1,self.clf.tree_.children_right == -1))
					self.folhas.append(folhas)
					# self.timestr = time.strftime("%Y%m%d-%H%M%S") # Se quiser salvar o arquivo de treinamento .joblib
    				# filename = "fileTrain"+self.timestr+".joblib"
    				# joblib.dump(self.clf,filename)

					tempo2 = datetime.datetime.now()
					diferenca = tempo2-tempo1 # para calcular o tempo de treinamento da ML
					print "Diferenca tempo -----------"
					print diferenca
					print (diferenca.seconds,":",diferenca.microseconds)
					# self.serieTempoML.append((diferenca.microseconds/1000.0)) #adiciona o tempo na serie em miliseconds
					self.serieTempoML.append(diferenca) #adiciona o tempo na serie em miliseconds

				erroML = numpy.abs(self.estimSVMR - self.serieTarget[-1])
				self.serieErroLQM3.append(erroML)
				self.startT = time.time()

			self.finalSerieML = self.serieML[-1]
			self.finalSerieML = numpy.arange(3).reshape(1,-1) # Para duas entradas, usar 	self.finalSerieML = numpy.arange(2).reshape(1,-1)
			self.estimSVMR = float(self.clf.predict(self.finalSerieML)) # Predizer somente o ultimo valor da serie		
			self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimSVMR))

			# prediction, bias, contributions = ti.predict(self.clf, self.finalSerieML) # lib treeinterpreter

			# for i in range(len(self.finalSerieML)):
			# 	print "Instance", i
			# 	print "Bias (trainset mean)", bias[i]
			# 	print "Feature contributions:"
			# 	for c, feature in sorted(zip(contributions[i], 
			#     	boston.feature_names), 
			#     	key=lambda x: -abs(x[0])):
			#         print feature, round(c, 2)
			#     print "-"*20



	def sma(self, values, window): # Simple Moving Average
		weights = numpy.repeat(1.0, window)/window
		sma = numpy.convolve(values, weights, 'valid')
		return sma


	def ema(self, data, window): # Exponential Moving Average
		"""
		Calculates Exponential Moving Average
		http://fxtrade.oanda.com/learn/forex-indicators/exponential-moving-average
		"""
		# Source: http://codereview.stackexchange.com/questions/70510/calculating-exponential-moving-average-in-python
		# See more about `alpha` in https://github.com/VividCortex/ewma
		# Now suppose that you wish to construct a EWMA whose samples have the same average age. The formula to compute
		# the alpha required for this is: alpha = 2/(N+1). Proof is in the book "Production and Operations Analysis" by
		# Steven Nahmias. So, for example, if you have a time-series with samples once per second, and you want to get
		# the moving average over the previous minute, you should use an alpha of .032786885. This, by the way, is the
		# constant alpha used for this repository's SimpleEWMA.

		if len(data) < 2 * window:
			raise ValueError("data is too short")
		c = 2.0 / (window + 1) # c = alpha (or constant)

		current_ema = self.sma(data[-window*2:-window], window)
		for value in data[-window:]:
			current_ema = (c * value) + ((1 - c) * current_ema)
		return current_ema


	def kalmanFilter(self, serie):

		# intial parameters
		n_iter = 10
		# WARNING: Minimum data inputs >= n_iter

		# print "\n--------------------- Kalman filter is use -------------------- \n"
		sz = (n_iter,) # size of array

		Q = 1e-5 # process variance
		z = serie # observations

		# allocate space for arrays
		xhat=numpy.zeros(sz)      # a posteri estimate of x
		P=numpy.zeros(sz)         # a posteri error estimate
		xhatminus=numpy.zeros(sz) # a priori estimate of x
		Pminus=numpy.zeros(sz)    # a priori error estimate
		K=numpy.zeros(sz)         # gain or blending factor


		R = 0.1**2 # estimate of measurement variance, change to see effect

		# intial guesses
		xhat[0] = 0.0
		P[0] = 1.0

		for k in range(1,n_iter):
			# time update
			xhatminus[k] = xhat[k-1]
			Pminus[k] = P[k-1]+Q

			# measurement update
			K[k] = Pminus[k]/( Pminus[k]+R )
			xhat[k] = xhatminus[k]+K[k]*(z[k]-xhatminus[k])
			P[k] = (1-K[k])*Pminus[k]

		return (xhat[9])


	def statSummary(self):

		if self.ackCount > 0:
			calcTxE = (float(self.ackCount)/self.geralSendOrder)*100.0
			calcRel = float(self.geralSends)/self.ackCount
		else:
			calcTxE = 0.0
			calcRel = 0.0

		if self.treinaML == True :
			dft=pd.DataFrame(self.matrix,columns=['rssi', 'prr', 'prr2', 'snr', 'txentrega', 'relacao','latencia-ms','potencia','estimation'])
			dft.to_csv('traces.csv',mode='a')


		linha=[]

		print "\n============================================================== "
		agora = datetime.datetime.now()
		print agora.strftime("%d/%m/%Y - %H:%M:%S")

		print "\n   :::  LQE SUMMARY  :::"
		if self.method == 1:
			print "        LQE: No method - Fixo no maximo gain"
		elif self.method == 2:
			print "        LQE: RSSI"
		elif self.method == 3:
			print "        LQE: PRR"
		elif self.method == 4:
			print "        LQE: PRR2 - full"
		elif self.method == 5:
			print "        LQE: ETX" #OLD PRR2 - sem RSSI"
		elif self.method == 6:
			print "        LQE: Traditional PRR+RSSI"
		elif self.method == 7:
			print "        LQE: LQL"
		elif self.method == 8:
			print "        LQE: LQM3"

		print "\n-   Envios solicitados: %d" %(self.geralSendOrder)
		print "-   Total de envios efetivos: %d" % (self.geralSends)
		print "-   Total geral de acks recebidos: %d" % (self.ackCount)
		print "-   Quantidade de retransmissões: %d" % (self.geralSends - self.geralSendOrder)
		print "-   Relação envios/pacotes recebidos: %6.2f" %(calcRel)
		print "-   Taxa de entrega: %6.2f percent" %(calcTxE)
		print "-   Tempo medio de recebimento de acks: %6.2f" %(numpy.mean(self.serieTempoTotalAck))
		print "-   Desvio padrao do tempo de recebimento de acks: %6.2f" %(numpy.std(self.serieTempoTotalAck, dtype=numpy.float64))


		if self.method == 77: #LQL OLD
			print "-   ------------------------------------"
			print "-   Erro medio Machine Learning LQL: %6.2f percent" %(numpy.mean(self.serieErroSVMRLQL))
			print "-   Tamanho serie erro ML LQL: %d entradas " %(len(self.serieErroSVMRLQL))
		elif self.method == 8: #LQM3
			print "-   ------------------------------------"
			print "-   Erro medio Machine Learning LQM3: %6.2f percent" %(numpy.mean(self.serieErroLQM3))
			print "-   Tamanho serie erro ML LQM3: %d entradas " %(len(self.serieErroLQM3))
			# print "-   Tempo medio para processar LQM3: %6.3f seconds" %(numpy.mean(self.serieTempoML))
			# print "-   Desvio padrao do tempo para processar LQM3: %6.2f" %(numpy.std(self.serieTempoML, dtype=numpy.float64))
			# print "-   Qtde de reducoes da serie LQM3: %d " %(self.contaReducao)
			print "-   Qtde de treinos da serie LQM3: %d " %(self.contaTreinos)
			print "-   Qtde de concept drift detectado: %6.2f" %(self.contaConceptDrift)
			print "-   Parametros da ML: "
			print self.clf.get_params(self)
			print "\n-   Depth da ML: " 
			print self.profund
			print "\n-   Leaves da ML: " 
			print self.folhas

		print "============================================================== \n"
		#print self.serieTempoTotalAck

		# ARQUIVOS CSV FORMATO PANDAS FRAME:

		linha.append(agora.strftime("%d/%m/%Y - %H:%M:%S")) #timestamp
		linha.append(self.method)
		linha.append(self.geralSendOrder) #enviosSolicitados
		linha.append(self.geralSends) #enviosEfetivos
		linha.append(self.ackCount) #acksRecebidos
		linha.append(self.geralSends - self.geralSendOrder) #retransmissoes
		linha.append(calcRel) #relacao
		linha.append(calcTxE) #taxaEntrega
		linha.append(numpy.mean(self.serieTempoTotalAck)) #tempoMedioRecebAck
		linha.append(numpy.std(self.serieTempoTotalAck, dtype=numpy.float64)) #desvioPadraoAck
		linha.append(self.contaTreinos) #qtde Treinos LQM3
		linha.append(self.contaConceptDrift) #qtde concept drift detectado
		linha.append(self.profund) # max depth ML Tree
		linha.append(self.folhas) # max leaves ML Tree

		matr = []
		matr.append(linha)

		dfstat=pd.DataFrame(matr,columns=['timestamp', 'method', 'enviosSolicitados', 'enviosEfetivos', 
			'acksRecebidos', 'retransmissoes','relacao','taxaEntrega','tempoMedioRecebAck','desvioPadraoAck','treinos','conceptDrift','depth','folhas'])
		# if file does not exist write header
		if not os.path.isfile('resultLQE.csv'):
		   dfstat.to_csv('resultLQE.csv',mode='a')
		else: # else it exists so append without writing the header
		   dfstat.to_csv('resultLQE.csv',mode='a', header=False)


	def holtwinters(self, y, alpha, beta, gamma, c, debug=False):
		"""
		y - time series data.
		alpha , beta, gamma - exponential smoothing coefficients
										  for level, trend, seasonal components.
		c -  extrapolated future data points.
			  4 quarterly
			  7 weekly.
			  12 monthly
		The length of y must be a an integer multiple  (> 2) of c.
		"""
		# Compute initial b and intercept using the first two complete c periods.
		ylen = len(y)
		if ylen % c != 0:
			return None
		fc = float(c)
		ybar2 = sum([y[i] for i in range(c, 2 * c)]) / fc
		ybar1 = sum([y[i] for i in range(c)]) / fc
		b0 = (ybar2 - ybar1) / fc
		if debug: print "b0 = ", b0

		# Compute for the level estimate a0 using b0 above.
		tbar = sum(i for i in range(1, c + 1)) / fc
		#print tbar
		a0 = ybar1 - b0 * tbar
		if debug: print "a0 = ", a0

		# Compute for initial indices
		I = [y[i] / (a0 + (i + 1) * b0) for i in range(0, ylen)]
		if debug: print "Initial indices = ", I

		S = [0] * (ylen + c)
		for i in range(c):
			S[i] = (I[i] + I[i + c]) / 2.0

		# Normalize so S[i] for i in [0, c)  will add to c.
		tS = c / sum([S[i] for i in range(c)])
		for i in range(c):
			S[i] *= tS
			if debug: print "S[", i, "]=", S[i]

		# Holt - winters proper ...
		if debug: print "Use Holt Winters formulae"
		F = [0] * (ylen + c)

		At = a0
		Bt = b0
		for i in range(ylen):
			Atm1 = At
			Btm1 = Bt
			At = alpha * y[i] / S[i] + (1.0 - alpha) * (Atm1 + Btm1)
			Bt = beta * (At - Atm1) + (1 - beta) * Btm1
			S[i + c] = gamma * y[i] / At + (1.0 - gamma) * S[i]
			F[i] = (a0 + b0 * (i + 1)) * S[i]
			#print "i=", i + 1, "y=", y[i], "S=", S[i], "Atm1=", Atm1, "Btm1=", Btm1, "At=", At, "Bt=", Bt, "S[i+c]=", S[
			 #   i + c], "F=", F[i]
			#print i, y[i], F[i]
		# Forecast for next c periods:
		# for m in range(c):
		#     print "forecast:", (At + Bt * (m + 1)) * S[ylen + m]

		m = c-1 # ultimo passo adiante de c
		estim = (At + Bt * (m + 1)) * S[ylen + m]

		return estim


		# the time-series data example
		#y = [146, 96, 59, 133, 192, 127, 79, 186, 272, 155, 98, 219]

		#holtwinters(y, 0.2, 0.1, 0.05, 4)
