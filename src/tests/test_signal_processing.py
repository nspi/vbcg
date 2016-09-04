#!/usr/bin/env python
# -*- coding: ascii -*-
"""test_signal_processing.py - tests for src/signal_processing.py"""

import unittest
import nose
import numpy as np

from signal_processing import SignalProcessor
from nose.tools import assert_is_instance, assert_false, assert_equal, assert_almost_equal


class Test(unittest.TestCase):

    def setUp(self):
        # Create instance
        self.signal_processor = SignalProcessor()

    def test__curveFit(self):
        m = self.signal_processor._SignalProcessor__curveFit([0, 1, 2, 3, 4], [0, 5, 10, 15, 20])
        assert_almost_equal(m[0], 5)

    def test_normalize(self):
        assert_is_instance(self.signal_processor.normalize(np.random.rand(100)), np.ndarray)

    def test_nextpow2(self):
        assert_equal(self.signal_processor.nextpow2(100), 128)

    def test_computeZeroPaddingValues(self):
        ret_1, ret_2 = self.signal_processor.computeZeroPaddingValues(128)
        assert_equal(ret_1, ret_2)

    def test_filterWaveform(self):
        ret_1, ret_2 = self.signal_processor.filterWaveform(np.random.rand(100),
                                                            np.random.rand(100),
                                                            np.random.randint(10) + 10,
                                                            np.random.randint(10) + 10,
                                                            0.5)
        assert_false(ret_1)
        assert_is_instance(ret_2, np.ndarray)

    def test_computeHR(self):
        ret_1, ret_2, ret_3, ret_4 = self.signal_processor.computeHR(np.random.rand(100), np.random.randint(10) + 10)
        assert_is_instance(ret_1, float)
        assert_is_instance(ret_2, np.ndarray)
        assert_is_instance(ret_3, np.ndarray)
        assert_is_instance(ret_4, int)


if __name__ == '__main__':
    nose.main()
