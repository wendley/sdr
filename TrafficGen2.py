#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Trafficgen2
# Generated: Tue Sep 25 16:33:43 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sys
import trafficgen
from gnuradio import qtgui


class TrafficGen2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Trafficgen2")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Trafficgen2")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "TrafficGen2")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

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
        self.trafficgen_generator_uniform_0 = trafficgen.generator_uniform(trafficgen.VBR_PORT_BURST_INTERVAL, 0, 0.3, 1000)
        self.trafficgen_generator_poisson_0 = trafficgen.generator_poisson(trafficgen.VBR_PORT_PACKET_SIZE, 0.5, 1000)
        self.trafficgen_generator_gaussian_0 = trafficgen.generator_gaussian(trafficgen.VBR_PORT_REQUEST_BURST_DURATION, 0.5, 0.1, 1000)
        self.trafficgen_generator_constant_0_0 = trafficgen.generator_constant(trafficgen.VBR_PORT_REQUEST_PACKET_INTERVAL, 200)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.trafficgen_generator_constant_0_0, 'Value'), (self.trafficgen_vbr_transmitter_0, 'Packet Interval'))
        self.msg_connect((self.trafficgen_generator_gaussian_0, 'Value'), (self.trafficgen_vbr_transmitter_0, 'Burst Duration'))
        self.msg_connect((self.trafficgen_generator_poisson_0, 'Value'), (self.trafficgen_vbr_transmitter_0, 'Packet Size'))
        self.msg_connect((self.trafficgen_generator_uniform_0, 'Value'), (self.trafficgen_vbr_transmitter_0, 'Burst Interval'))
        self.msg_connect((self.trafficgen_vbr_transmitter_0, 'Request'), (self.trafficgen_generator_constant_0_0, 'Request'))
        self.msg_connect((self.trafficgen_vbr_transmitter_0, 'Request'), (self.trafficgen_generator_gaussian_0, 'Request'))
        self.msg_connect((self.trafficgen_vbr_transmitter_0, 'Request'), (self.trafficgen_generator_poisson_0, 'Request'))
        self.msg_connect((self.trafficgen_vbr_transmitter_0, 'Request'), (self.trafficgen_generator_uniform_0, 'Request'))
        self.msg_connect((self.trafficgen_vbr_transmitter_0, 'PDU'), (self.trafficgen_receiver_0, 'input'))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "TrafficGen2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


def main(top_block_cls=TrafficGen2, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
