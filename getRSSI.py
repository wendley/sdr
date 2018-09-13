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


import numpy, pmt
from numpy import convolve
from gnuradio import gr
from gnuradio import uhd
from sklearn import svm


class getRSSI(gr.sync_block):
	"""
	Estimates the Link Quality using RSSI, PRR or PRR2.
	[1] https://github.com/osh/gr-uhdgps
	[2] https://github.com/osh/gr-eventstream
	"""

	def __init__(self, printPower=False, method=1, filters=1, window=40, minRSSI=-100, maxRSSI=-56, alphaHW=0.2, betaHW=0.1, gammaHW=0.05):
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


		self.serie=[]
		self.seriePRR=[]
		self.serieACK=[]
		self.serieLACK=[] # Long range window
		self.seriePCK=[]
		self.serieLPCK=[] # Long range
		self.serieML=[] # For Machine Learning fit
		self.serieSNR=[]
		self.estimSVMR = 0.0
		self.tempML = []
		self.serieTarget=[]
		self.finalSerieML = []
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
		self.geralSends = 0 # Total number of sends
		self.geralSendOrder = -1 # Total number of send orders
		self.mediaSNR = 0.0

		self.fnRSSI="/home/wendley/Experimentos/SerieRSSI.txt"
		self.fnRSSIKalman="/home/wendley/Experimentos/SerieRSSIKalman.txt"
		self.fnPRR="/home/wendley/Experimentos/SeriePRR.txt"
		self.fnPRRRssi="/home/wendley/Experimentos/SeriePRRRssi.txt"
		self.fnPRR2levels="/home/wendley/Experimentos/SeriePRR2levels.txt"
		self.fnPRR2="/home/wendley/Experimentos/SeriePRR2.txt"

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

		self.clf = svm.SVR()

	def work(self, input_items, output_items):
		assert (False)


	def handler(self, pdu):
		self.Rssi = pmt.to_python(pdu)

		if self.filter == 3: # Kalman
			if len(self.serie) < self.window*4:
				self.serie.append(self.Rssi)
			else:
				self.serie.append(self.Rssi)
				del(self.serie[0])

			if len(self.serie) > 10:
				self.kRssi = self.kalmanFilter(self.serie)
				# print "\n ------- RSSI with Kalman filter: %6.2f ----- \n"  % (self.kRssi)
				# print type (self.kRssi)

		else:
			if self.printPower: print "Potencia do meio: %6.2f dB" % (self.Rssi)

			# Cria janela móvel limitada (para não extrapolar a memória) para cálculo das médias
			self.serie.append(self.Rssi)
			if len(self.serie) > self.window*4:
				del(self.serie[0])

			if len(self.serie)>2*self.window/2: # limitação da EMA
				self.emaRssi = self.ema(self.serie, self.window/2)


	def handlerAck(self, pdu):
		tipo = pmt.to_python(pdu)

		if tipo == 1: # Sinaliza recebimento de um ack
			self.ackCount += 1
			# print "\n--------- \nTotal geral de acks recebidos: %d \n--------- \n" % (self.ackCount)
			self.sendedPacks += 1
			self.calcPRR(1)
			self.calcLQE()
		elif tipo == 999: # Sinaliza final de arquivo ou de msg, após esvaziar buffer do MAC
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
		self.calcLQE()

		# Salva arquivos para scatterplot
		arq1 = open(self.fnRSSI, "a")
		arq1.write(str(self.estimRssi)+'\n')

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
				print "\n--------- \nLONG PRR: %2.4f\n---------\n" % (float(self.geralLPRR))
				# print "\n--------- \nLONG PRR LENGTH: %2.4f\n---------\n" % (float(len(self.serieLACK)))


		elif self.filter == 2:
			# Exponential Moving Average filter
			self.geralPRR = self.preEMA(self.serieACK,self.seriePCK, self.window/2)  # PRR from short range

			if self.method == 4 or self.method == 5 or self.method == 7 or self.method == 8: # PRR 2 levels
				self.geralLPRR = self.preEMA(self.serieLACK, self.serieLPCK, self.window*4) # PRR from long range
				print "\n--------- \nLONG PRR: %2.4f\n---------\n" % (float(self.geralLPRR))
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

		if tempRssi < minRSSI :
			tempRssi = minRSSI
		elif tempRssi > maxRSSI :
			tempRssi = maxRSSI

		tempKalmanRssi= self.kRssi

		if tempKalmanRssi < minRSSI :
			tempKalmanRssi = minRSSI
		elif tempKalmanRssi > maxRSSI :
			tempKalmanRssi = maxRSSI

		self.estimRssi = float(1-(tempRssi-minRSSI)/rangeRSSI)

		self.estimRssiKalman = float(1-(tempKalmanRssi-minRSSI)/rangeRSSI)


		# RSSI Instantaneo + Kalman kRssi
		# See calibration in datasheet of AD9361 (Analog Device of B210):
		# http://www.analog.com/media/en/technical-documentation/user-guides/AD9361_Reference_Manual_UG-570.pdf

		self.estimPRR = float(self.geralPRR)
		self.estimPRR_Rssi = float(min(self.geralPRR, self.estimRssi)) # PRR + RSSI

		self.estimPRR2levels = float(min(self.geralPRR,self.geralLPRR)) # PRR with 2 levels without RSSI
		self.estimPRR2 = float(min(self.geralPRR,self.geralLPRR, self.estimRssi)) # PRR2 Full
		# print "DEBUG---------- IMPRIMINDO SERIE-ESTIM-PRR2 desmembrada -----------"
		# print(self.geralPRR)
		# print(self.geralLPRR)
		# print(self.estimRssi)




		if self.method == 1:
			# No estimator - constant gain
			print "No estimator in use - the tx gain is constant"

		elif self.method == 2:
			# Estimator using ONLY RSSI:

			if self.filter == 2: #EMA
				self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimRssi))
			elif self.filter == 3: #Kalman
				self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimRssiKalman))

			#print "RSSI method in use"
			#This sets the gain
			# FIXME
			aux = float(self.emaRssi)
			#print "RSSI ------------ %2.4f\n" % (float(aux))
			# self.message_port_pub(pmt.intern("estimation"), pmt.from_double(self.gainTx))

		elif self.method == 3:
			# Estimator using ONLY traditional PRR:

			if self.filter == 3: #Kalman
				print "\n--- WARNING: Kalman filter only for RSSI. Using EMA --- \n"

			# self.gainTx = self.holtwinters(self.serie, self.alphaHW, self.betaHW, self.gammaHW, 4)
			# if self.geralPRR < 0.699:
			# 	self.gainTx = 89
			# else:
			# 	self.gainTx = 89 - (self.geralPRR-0.7)*100

			# self.estim = self.geralPRR

			#print "PRR method in use"
			#This sets the gain
			# est=float(self.estim)
			self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimPRR))

		elif self.method == 4:
			# PRR 2 levels + RSSI (FULL)

			# if self.geralPRR < 0.699 or self.geralLPRR < 0.699:
			# 	self.estim = 0
			# else:
				#self.gainTx = max(89 - min((self.geralPRR-0.7)*100,(self.geralLPRR-0.7)*100),(170+int(self.emaRssi)+72)*0.46)

			# self.estim = float(min(self.geralPRR,self.geralLPRR, self.emaRssi))
			# self.geralPRR2 = self.estim

			#print "Proposed mode in use - under development - the tx gain is constant"
			#This sets the gain
			#gTx=float(self.gainTx)
			self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimPRR2))

		elif self.method == 5:
			# PRR 2 levels without RSSI

			# self.estim = float(min(self.geralPRR,self.geralLPRR))
			# self.geralPRR2modif = self.estim

			self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimPRR2levels))

			#print "Dynamic mode in use - under development - the tx gain is constant"

		elif self.method == 6:
			# Traditional PRR + RSSI
			self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimPRR_Rssi))

		elif self.method == 7:
			# Foresee 4C (like)
			print "Foresee ainda nao implementado"

		elif self.method == 8:
			# Machine Learning SVMR
			#####################################################
			#													#
			# IDEA: Construcao da serie para Machine Learning:	#
			#													#
			#####################################################

			if len(self.serieML) >= 20: # Arbitrary value to training
				del(self.serieML[0])
				# del(self.tempML[0])
				del(self.serieTarget[0])

			self.tempML.append(self.estimPRR)
			self.tempML.append(self.estimRssi)
			self.tempML.append(self.mediaSNR)
			self.serieML.append(list(self.tempML))
			self.tempML=[]
			self.serieTarget.append(self.estimPRR2)
			self.finalSerieML = numpy.array(self.serieML)

			#SVMR

			print "DEBUG---------- IMPRIMINDO SERIE-ML -----------"
			print(self.serieML)
			#print "DEBUG---------- IMPRIMINDO SERIE-TARGET -----------"
			#print(self.serieTarget)
			# estimSVMR = 0.0 #: FIXME Corrigir logica
			if len(self.serieML) >= 10:
				self.finalSerieML=numpy.array(self.serieML)
				# print "---------- IMPRIMINDO SERIE-ML-ARRAY -----------"
				# print(self.finalSerieML)

				# print "---------- IMPRIMINDO SERIE-TARGET-ML-ARRAY -----------"
				# print(self.serieTarget)

				self.clf.fit(self.serieML[:-1],self.serieTarget[:-1]) # Treina com todos os dados da serie, exceto o último
				self.finalSerieML = self.serieML[-1]
				self.finalSerieML = numpy.arange(3).reshape(1,-1) # Para duas entradas, usar 	self.finalSerieML = numpy.arange(2).reshape(1,-1)
				self.estimSVMR = float(self.clf.predict(self.finalSerieML)) # Predizer somente o ultimo valor da serie
				erroSVMR = self.estimSVMR - self.serieTarget[-1]
				print "ESTIMATIVA GERADA PELA ML-SVMR: %f" %self.estimSVMR
				print "ERRO do SVMR: %f" %erroSVMR


			#---------------

			# print "ESTIMATIVA GERADA PELA ML-SVMR: %f" %self.estimSVMR
			self.message_port_pub(pmt.intern("estimation"),pmt.from_double(self.estimSVMR))



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



		print "\n============================================================== "
		print "   :::  LQE SUMMARY  :::"
		print "\n-   Envios solicitados: %d" %(self.geralSendOrder)
		print "-   Total de envios efetivos: %d" % (self.geralSends)
		print "-   Total geral de acks recebidos: %d" % (self.ackCount)
		print "-   Quantidade de retransmissões: %d" % (self.geralSends - self.geralSendOrder)
		print "-   Relação envios/pacotes recebidos: %6.2f" %(calcRel)
		print "-   Taxa de entrega: %6.2f percent" %(calcTxE)
		print "============================================================== \n"


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
