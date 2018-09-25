#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Trafficgen2
# Generated: Tue Sep 25 10:53:29 2018
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import trafficgen


class TrafficGen2(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Trafficgen2")

        ##################################################
        # Blocks
        ##################################################
        self.trafficgen_vbr_transmitter_0 = trafficgen.vbr_transmitter(True,
        		trafficgen.CONTENT_CONSTANT,
        		0,
        		0,
        		255,
        		'/tmp/trafficgen_vbr_transmitter.log')
        self.trafficgen_receiver_0 = trafficgen.receiver('/tmp/trafficgen_receiver.log')
        self.trafficgen_generator_uniform_0 = trafficgen.generator_uniform(trafficgen.VBR_PORT_REQUEST_PACKET_INTERVAL, 0, 1, 1000)
        self.trafficgen_generator_poisson_0 = trafficgen.generator_poisson(trafficgen.VBR_PORT_PACKET_SIZE, 0.5, 1000)
        self.trafficgen_generator_gaussian_0 = trafficgen.generator_gaussian(trafficgen.VBR_PORT_REQUEST_BURST_DURATION, 0.5, 0.1, 1000)
        self.trafficgen_generator_constant_0 = trafficgen.generator_constant(trafficgen.VBR_PORT_BURST_INTERVAL, 300)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.trafficgen_generator_constant_0, 'Value'), (self.trafficgen_vbr_transmitter_0, 'Burst Interval'))
        self.msg_connect((self.trafficgen_generator_gaussian_0, 'Value'), (self.trafficgen_vbr_transmitter_0, 'Burst Duration'))
        self.msg_connect((self.trafficgen_generator_poisson_0, 'Value'), (self.trafficgen_vbr_transmitter_0, 'Packet Size'))
        self.msg_connect((self.trafficgen_generator_uniform_0, 'Value'), (self.trafficgen_vbr_transmitter_0, 'Packet Interval'))
        self.msg_connect((self.trafficgen_vbr_transmitter_0, 'Request'), (self.trafficgen_generator_constant_0, 'Request'))
        self.msg_connect((self.trafficgen_vbr_transmitter_0, 'Request'), (self.trafficgen_generator_gaussian_0, 'Request'))
        self.msg_connect((self.trafficgen_vbr_transmitter_0, 'Request'), (self.trafficgen_generator_poisson_0, 'Request'))
        self.msg_connect((self.trafficgen_vbr_transmitter_0, 'Request'), (self.trafficgen_generator_uniform_0, 'Request'))
        self.msg_connect((self.trafficgen_vbr_transmitter_0, 'PDU'), (self.trafficgen_receiver_0, 'input'))


def main(top_block_cls=TrafficGen2, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
