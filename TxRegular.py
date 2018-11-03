#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: IEEE 802.15.4 Transceiver using OQPSK PHY
# Generated: Sat Nov  3 16:22:07 2018
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from ieee802_15_4_oqpsk_phy import ieee802_15_4_oqpsk_phy  # grc-generated hier_block
from optparse import OptionParser
import es
import foo
import ieee802_15_4
import lqe
import pmt
import time
import uhdgps


class TxRegular(gr.top_block):

    def __init__(self, freq=2480000000, gain=48, method=7):
        gr.top_block.__init__(self, "IEEE 802.15.4 Transceiver using OQPSK PHY")

        ##################################################
        # Parameters
        ##################################################
        self.freq = freq
        self.gain = gain
        self.method = method

        ##################################################
        # Blocks
        ##################################################
        self.uhdgps_cpdu_average_power_0 = uhdgps.cpdu_average_power(-60)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(('', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(5000000)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(('', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(5000000)
        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.lqe_powerControl_0 = lqe.powerControl(gain, '/home/wendley/SerieGanho100ms.txt', False)
        self.lqe_getRSSI_0 = lqe.getRSSI(False, 2, 2, 40, -108, -67, 0.500, 0.2, 0.1, 0.05)
        self.ieee802_15_4_rime_stack_0 = ieee802_15_4.rime_stack(([129]), ([131]), ([132]), ([23,42]))
        self.ieee802_15_4_oqpsk_phy_0 = ieee802_15_4_oqpsk_phy()
        self.ieee802_15_4_mac_0 = ieee802_15_4.mac(True)
        self.foo_periodic_msg_source_1 = foo.periodic_msg_source(pmt.intern("0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"), 400, 1000, True, False)
        self.es_trigger_sample_timer_0 = es.trigger_sample_timer(gr.sizeof_gr_complex, int(2000), 2, int(4000000), 512 )
        self.es_sink_0 = es.sink(1*[gr.sizeof_gr_complex],8,64,0,2,0)
        self.es_handler_pdu_0 = es.es_make_handler_pdu(es.es_handler_print.TYPE_C32)
        self.digital_probe_mpsk_snr_est_c_0 = digital.probe_mpsk_snr_est_c(2, 1000, 0.001)
        self.blocks_socket_pdu_0_0 = blocks.socket_pdu("UDP_SERVER", '', '52001', 10000, False)
        self.blocks_pdu_remove_0 = blocks.pdu_remove(pmt.intern("es::event_buffer"))

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_pdu_remove_0, 'pdus'), (self.ieee802_15_4_mac_0, 'cs in'))
        self.msg_connect((self.blocks_socket_pdu_0_0, 'pdus'), (self.ieee802_15_4_rime_stack_0, 'bcin'))
        self.msg_connect((self.digital_probe_mpsk_snr_est_c_0, 'snr'), (self.lqe_getRSSI_0, 'SNR'))
        self.msg_connect((self.es_handler_pdu_0, 'pdus_out'), (self.uhdgps_cpdu_average_power_0, 'cpdus'))
        self.msg_connect((self.es_trigger_sample_timer_0, 'sample_timer_event'), (self.es_handler_pdu_0, 'handle_event'))
        self.msg_connect((self.es_trigger_sample_timer_0, 'which_stream'), (self.es_sink_0, 'schedule_event'))
        self.msg_connect((self.foo_periodic_msg_source_1, 'out'), (self.ieee802_15_4_rime_stack_0, 'bcin'))
        self.msg_connect((self.foo_periodic_msg_source_1, 'out'), (self.lqe_getRSSI_0, 'sendOrder'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'pdu out'), (self.ieee802_15_4_oqpsk_phy_0, 'txin'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'app out'), (self.ieee802_15_4_rime_stack_0, 'fromMAC'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'ackOut'), (self.lqe_getRSSI_0, 'Ackin'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'packLost'), (self.lqe_getRSSI_0, 'lostPacks'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'resendPck'), (self.lqe_getRSSI_0, 'sendPacks'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'ackOut'), (self.lqe_powerControl_0, 'saveGain'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'resendPck'), (self.lqe_powerControl_0, 'saveGain'))
        self.msg_connect((self.ieee802_15_4_oqpsk_phy_0, 'rxout'), (self.ieee802_15_4_mac_0, 'pdu in'))
        self.msg_connect((self.ieee802_15_4_rime_stack_0, 'bcout'), (self.blocks_socket_pdu_0_0, 'pdus'))
        self.msg_connect((self.ieee802_15_4_rime_stack_0, 'toMAC'), (self.ieee802_15_4_mac_0, 'app in'))
        self.msg_connect((self.lqe_getRSSI_0, 'estimation'), (self.lqe_powerControl_0, 'estimation'))
        self.msg_connect((self.uhdgps_cpdu_average_power_0, 'cpdus'), (self.blocks_pdu_remove_0, 'pdus'))
        self.msg_connect((self.uhdgps_cpdu_average_power_0, 'rssi'), (self.lqe_getRSSI_0, 'RSSIin'))
        self.connect((self.es_trigger_sample_timer_0, 0), (self.es_sink_0, 0))
        self.connect((self.ieee802_15_4_oqpsk_phy_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.digital_probe_mpsk_snr_est_c_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.es_trigger_sample_timer_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.ieee802_15_4_oqpsk_phy_0, 0))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_gain(self.gain, 0)

        self.uhd_usrp_sink_0.set_gain(self.gain, 0)


    def get_method(self):
        return self.method

    def set_method(self, method):
        self.method = method


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(2480000000),
        help="Set freq [default=%default]")
    parser.add_option(
        "", "--method", dest="method", type="intx", default=7,
        help="Set method [default=%default]")
    return parser


def main(top_block_cls=TxRegular, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls(freq=options.freq, method=options.method)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
