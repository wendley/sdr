#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
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

import numpy, pmt
from gnuradio import gr
from gnuradio import uhd

class powerControl(gr.sync_block):
    """
    Control the transmitter power according an estimation varying between 0 and 1.
    """
    def __init__(self, igtx=0, filenameG="/tmp/seriesG.txt", randomGain=False):
        gr.sync_block.__init__(self,
            name="Power Control",
            in_sig=[],
            out_sig=[])


        self.gainTx = igtx # arbitrary initial gain tx
        self.count = 0
        self.fn = filenameG
        self.rGain = randomGain
        self.serieGain = []
        self.cont999 = 1


        self.uhd_usrp_sink = \
        uhd.usrp_sink(device_addr="",stream_args=uhd.stream_args('fc32'))

        if self.count ==0 :
            self.uhd_usrp_sink.set_gain(self.gainTx) #This sets the initial gain only once time

        self.message_port_register_in(pmt.intern("saveGain"))
        self.message_port_register_in(pmt.intern("estimation"))

        self.set_msg_handler(pmt.intern("estimation"), self.handler)
        self.set_msg_handler(pmt.intern("saveGain"), self.handlerG)


    def work(self, input_items, output_items):
        assert (False)


    def handler(self,pdu):
        estimativa = pmt.to_float(pdu) #Estimativa entre 0,0 e 1,0
        # print "Estimativa: --- %6.2f" % (estimativa)

        newGain = 25*(1-estimativa)+45 #Normalização  70 - 45 = 25 --- 45 foi o minimo gain para tx
        newGain = 46 # usado para fixar o valor durante a calibração
        # print "Ganho de Tx: --- %6.2f" % (newGain)
        # https://www.analog.com/media/en/technical-documentation/data-sheets/AD9361.pdf

        self.uhd_usrp_sink.set_gain(newGain) #This sets the gain



    def handlerG(self,pdu): # To save the gain series in file:

        if pmt.to_float(pdu) != 999 and pmt.to_float(pdu) != 1 and pmt.to_float(pdu) != 0:
            self.count = self.count + 1

            # RANDOM GAIN:
            if self.rGain :
                nGain = numpy.random.randint(0,89) # RANDOM gain
                self.uhd_usrp_sink.set_gain(nGain) #This sets the RANDOM gain

            ganho = self.uhd_usrp_sink.get_gain() # This verifies the gain value on USRP
            #print "Ganho no USRP: %d" %(int(ganho))

            self.serieGain.append(ganho)

            #print "Ganho TX %d" % (ganho)

            # arql = open(self.fn, "a")
            # arql.write(str(ganho)+'\n')

        elif pmt.to_float(pdu) == 999: # Sinaliza fim de arquivo e fila no mac vazia
            if self.cont999 == 1:
                self.cont999 = 2
            elif self.cont999 == 2: #faz com que somente no segundo 999 (do buffer) eh que haja a chamada do stat
                self.statSummary()

    def statSummary(self):

        print "\n============================================================== "
        print "   :::  POWER CONTROL SUMMARY  :::"
        print "\n-   Média dos ganhos das transmissões: %6.2f" %(numpy.mean(self.serieGain))
        print "-   Desvio padrão: %6.2f" %(numpy.std(self.serieGain))
        print "-   Tamanho da amostra: %d" %len(self.serieGain)
        print "============================================================== \n"
