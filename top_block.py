#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Mon Sep 25 13:31:36 2017
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

from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 5e6
        self.rxgain = rxgain = 0
        self.cfreq = cfreq = 105.7e6

        ##################################################
        # Blocks
        ##################################################
        _rxgain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rxgain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_rxgain_sizer,
        	value=self.rxgain,
        	callback=self.set_rxgain,
        	label='RX Gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rxgain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_rxgain_sizer,
        	value=self.rxgain,
        	callback=self.set_rxgain,
        	minimum=0,
        	maximum=20,
        	num_steps=20,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_rxgain_sizer)
        _cfreq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._cfreq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_cfreq_sizer,
        	value=self.cfreq,
        	callback=self.set_cfreq,
        	label='Center Frequency',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._cfreq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_cfreq_sizer,
        	value=self.cfreq,
        	callback=self.set_cfreq,
        	minimum=50e6,
        	maximum=150e6,
        	num_steps=10,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_cfreq_sizer)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=cfreq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(cfreq, 0)
        self.uhd_usrp_source_0.set_gain(rxgain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=250,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(20, firdes.low_pass(
        	1, samp_rate, 100e3, 10e3, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=250e3,
        	audio_decimation=1,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 10e3, firdes.WIN_HAMMING, 6.76))

    def get_rxgain(self):
        return self.rxgain

    def set_rxgain(self, rxgain):
        self.rxgain = rxgain
        self._rxgain_slider.set_value(self.rxgain)
        self._rxgain_text_box.set_value(self.rxgain)
        self.uhd_usrp_source_0.set_gain(self.rxgain, 0)


    def get_cfreq(self):
        return self.cfreq

    def set_cfreq(self, cfreq):
        self.cfreq = cfreq
        self._cfreq_slider.set_value(self.cfreq)
        self._cfreq_text_box.set_value(self.cfreq)
        self.wxgui_fftsink2_0.set_baseband_freq(self.cfreq)
        self.uhd_usrp_source_0.set_center_freq(self.cfreq, 0)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
