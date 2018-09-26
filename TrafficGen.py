#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Trafficgen
# Generated: Wed Sep 26 14:56:44 2018
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
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sys
import trafficgen
from gnuradio import qtgui


class TrafficGen(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Trafficgen")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Trafficgen")
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

        self.settings = Qt.QSettings("GNU Radio", "TrafficGen")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.trafficgen_time_trigger_0 = trafficgen.time_trigger(True, 1000, 1000)
        self.trafficgen_cbr_transmitter_0 = trafficgen.cbr_transmitter(100,
        		1500,
        		True,
        		trafficgen.CONTENT_CONSTANT,
        		1,
        		trafficgen.DIST_UNIFORM,
        		0,
        		255,
        		127,
        		42,
        		1,
        		1,
        		'/tmp/trafficgen_cbr_transmitter.log')
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.trafficgen_cbr_transmitter_0, 'PDU'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.trafficgen_time_trigger_0, 'trigger'), (self.trafficgen_cbr_transmitter_0, 'Trigger Start'))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "TrafficGen")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def main(top_block_cls=TrafficGen, options=None):

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
