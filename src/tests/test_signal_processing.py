#!/usr/bin/env python
# -*- coding: ascii -*-
"""test_signal_processing.py - tests for src/signal_processing.py"""

import unittest
import nose
import numpy as np
import settings
import time

from defines import *
from signal_processing import SignalProcessor
from nose.tools import assert_is_instance, assert_false, assert_equal, assert_almost_equal, assert_true


class Test(unittest.TestCase):

    def setUp(self):
        # Create instance
        self.signal_processor = SignalProcessor()

    def tearDown(self):
        # Clear instance
        self.signal_processor.clear()

    def test__curve_fit(self):
        m = self.signal_processor._SignalProcessor__curve_fit([0, 1, 2, 3, 4], [0, 5, 10, 15, 20])
        assert_almost_equal(m[0], 5)

    def test_normalize(self):
        assert_is_instance(self.signal_processor.normalize(np.random.rand(100)), np.ndarray)

    def test_nextpow2(self):
        assert_equal(self.signal_processor.nextpow2(100), 128)

    def test_compute_zero_padding_values(self):
        ret_1, ret_2 = self.signal_processor.compute_zero_padding_values(128)
        assert_equal(ret_1, ret_2)

    def test_filter_waveform_return_false(self):
        ret_1, ret_2 = self.signal_processor.filter_waveform(np.random.rand(100),
                                                             np.random.rand(100),
                                                             np.random.randint(10) + 10,
                                                             np.random.randint(10) + 10,
                                                             0.5)
        assert_false(ret_1)
        assert_is_instance(ret_2, np.ndarray)

    def test_filter_waveform_return_true(self):
        # Create random input signal
        input_signal = np.random.rand(100)
        # Initialize second signal
        input_signal_2 = np.ones(1)

        # This configuration of filter_waveform() should return true
        # (if time passed is > 0.5 and input_signal_2 is stable for 3 values)
        for num in range(0, 4):
            self.ret_1, self.ret_2 = self.signal_processor.filter_waveform(input_signal,
                                                                 input_signal_2,
                                                                 9,
                                                                 3,
                                                                 0.5)
            input_signal_2 = self.ret_2
            time.sleep(0.5)

        assert_true(self.ret_1)
        assert_is_instance(self.ret_2, np.ndarray)

    def test_compute_heart_rate_without_zero_padding(self):
        ret_1, ret_2, ret_3, ret_4 = self.signal_processor.compute_heart_rate(np.random.rand(100),
                                                                              np.random.randint(10) + 10)
        assert_is_instance(ret_1, float)
        assert_is_instance(ret_2, np.ndarray)
        assert_is_instance(ret_3, np.ndarray)
        assert_is_instance(ret_4, int)

    def test_compute_heart_rate_with_zero_padding(self):
        settings.flip_parameter(IDX_ZERO_PADDING)

        ret_1, ret_2, ret_3, ret_4 = self.signal_processor.compute_heart_rate(np.random.rand(100),
                                                                              np.random.randint(10) + 10)
        assert_is_instance(ret_1, float)
        assert_is_instance(ret_2, np.ndarray)
        assert_is_instance(ret_3, np.ndarray)
        assert_is_instance(ret_4, int)

        settings.flip_parameter(IDX_ZERO_PADDING)


if __name__ == '__main__':
    nose.main()
