#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
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

class contador(gr.sync_block):
    """
    Bloco contador: utilizado para limitar a quantidade de mensagens enviadas
    """
    def __init__(self,maxValor):
        gr.sync_block.__init__(self,
            name="contador",
            in_sig=[],
            out_sig=[])

        self.maxValor = int(maxValor)

        self.conta = 0
        self.message_port_register_in(pmt.intern("in"))
        self.message_port_register_out(pmt.intern("out"))
        self.set_msg_handler(pmt.intern("in"), self.handler)

    def work(self, input_items, output_items):
        assert (False)

    def handler(self, pdu): # Acionado sempre que chega uma msg
        msg = pmt.to_python(pdu)
        print ("Valor self conta: ")
        print (self.conta)

        if self.conta < self.maxValor :
            self.message_port_pub(pmt.intern("out"), pmt.to_pmt(msg))
            print ("MSG: ")
            print (msg)
        else:
            self.message_port_pub(pmt.intern("out"), pmt.get_PMT_EOF())

        self.conta +=1;
